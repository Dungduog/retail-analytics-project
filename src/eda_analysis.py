"""EDA cho tám câu hỏi nghiên cứu và các biểu đồ cốt lõi của dự án."""

from __future__ import annotations

from pathlib import Path
from typing import Union

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def _save_table(table: pd.DataFrame, output_dir: Path, name: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    table.to_csv(output_dir / name, index=False)


def _currency(value: float) -> str:
    return f"{value:,.2f}"


def run_eda(
    cleaned_file: Union[str, Path],
    customer_file: Union[str, Path],
    tables_dir: Union[str, Path],
    figures_dir: Union[str, Path],
    report_file: Union[str, Path],
) -> dict[str, pd.DataFrame]:
    """Tạo bảng EDA, biểu đồ và báo cáo insight từ dữ liệu đã làm sạch."""
    cleaned_path = Path(cleaned_file)
    customer_path = Path(customer_file)
    tables_path = Path(tables_dir)
    figures_path = Path(figures_dir)
    report_path = Path(report_file)

    data = pd.read_csv(cleaned_path, parse_dates=["InvoiceDate"])
    customers = pd.read_csv(customer_path)
    cancelled_mask = data["IsCancelled"].astype(str).str.lower().eq("true")
    sales = data[~cancelled_mask].copy()
    cancellations = data[cancelled_mask].copy()

    figures_path.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Doanh thu theo thời gian.
    monthly_revenue = (
        sales.groupby("OrderMonth", as_index=False)["Revenue"]
        .sum()
        .sort_values("OrderMonth")
    )
    _save_table(monthly_revenue, tables_path, "monthly_revenue.csv")

    # 2-3. Sản phẩm theo số lượng và doanh thu.
    product_sales = sales.dropna(subset=["Description"]).copy()
    top_products_quantity = (
        product_sales.groupby(["StockCode", "Description"], as_index=False)[
            "Quantity"
        ]
        .sum()
        .sort_values("Quantity", ascending=False)
        .head(20)
    )
    top_products_revenue = (
        product_sales.groupby(["StockCode", "Description"], as_index=False)[
            "Revenue"
        ]
        .sum()
        .sort_values("Revenue", ascending=False)
        .head(20)
    )
    _save_table(top_products_quantity, tables_path, "top_products_quantity.csv")
    _save_table(top_products_revenue, tables_path, "top_products_revenue.csv")

    # 4. Phân khúc giá theo tứ phân vị của UnitPrice trong normal sales.
    q1, median, q3 = sales["UnitPrice"].quantile([0.25, 0.50, 0.75]).tolist()
    price_bins = [-np.inf, q1, median, q3, np.inf]
    price_labels = ["Low", "Medium", "High", "Premium"]
    sales["PriceSegment"] = pd.cut(
        sales["UnitPrice"],
        bins=price_bins,
        labels=price_labels,
        include_lowest=True,
    )
    price_segments = (
        sales.groupby("PriceSegment", observed=True)
        .agg(
            Quantity=("Quantity", "sum"),
            Revenue=("Revenue", "sum"),
            TransactionLines=("InvoiceNo", "size"),
        )
        .reset_index()
    )
    price_segments["LowerBound"] = [-np.inf, q1, median, q3]
    price_segments["UpperBound"] = [q1, median, q3, np.inf]
    _save_table(price_segments, tables_path, "price_segments.csv")

    # 5. Khách hàng vừa chi tiêu nhiều vừa mua thường xuyên.
    top_customers = (
        customers[customers["Segment"] == "Champions"]
        .sort_values(["Monetary", "Frequency"], ascending=False)
        .head(20)
    )
    _save_table(top_customers, tables_path, "top_customers.csv")

    # 6. Doanh thu theo quốc gia.
    country_revenue = (
        sales.groupby("Country", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
    )
    _save_table(country_revenue, tables_path, "country_revenue.csv")

    # 7. Khách hàng lâu không quay lại.
    inactive_customers = (
        customers[customers["Segment"].isin(["Lost", "At Risk"])]
        .sort_values(["Recency", "Monetary"], ascending=[False, False])
        .head(20)
    )
    _save_table(inactive_customers, tables_path, "inactive_customers.csv")

    # 8. Sản phẩm xuất hiện nhiều trong cancellation invoices.
    cancelled_products = (
        cancellations.dropna(subset=["Description"])
        .groupby(["StockCode", "Description"], as_index=False)
        .agg(
            CancelledInvoiceCount=("InvoiceNo", "nunique"),
            CancelledRows=("InvoiceNo", "size"),
            CancelledQuantity=("Quantity", lambda values: values.abs().sum()),
            CancelledValue=("Revenue", lambda values: values.abs().sum()),
        )
        .sort_values(
            ["CancelledInvoiceCount", "CancelledQuantity"],
            ascending=False,
        )
        .head(20)
    )
    _save_table(cancelled_products, tables_path, "cancelled_products.csv")

    # Giá trị đơn hàng được tính ở cấp InvoiceNo, không phải từng dòng sản phẩm.
    order_values = (
        sales.groupby("InvoiceNo", as_index=False)["Revenue"]
        .sum()
        .rename(columns={"Revenue": "OrderValue"})
    )
    _save_table(order_values, tables_path, "order_values.csv")

    plt.style.use("seaborn-v0_8-whitegrid")

    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(
        monthly_revenue["OrderMonth"],
        monthly_revenue["Revenue"],
        marker="o",
        linewidth=2,
        color="#2F6690",
    )
    ax.set_title("Monthly Gross Revenue")
    ax.set_xlabel("Order month")
    ax.set_ylabel("Revenue")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(figures_path / "monthly_revenue.png", dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(15, 7))
    quantity_chart = top_products_quantity.head(10).sort_values("Quantity")
    revenue_chart = top_products_revenue.head(10).sort_values("Revenue")
    axes[0].barh(quantity_chart["Description"], quantity_chart["Quantity"], color="#3A7D44")
    axes[0].set_title("Top Products by Quantity")
    axes[0].set_xlabel("Quantity")
    axes[1].barh(revenue_chart["Description"], revenue_chart["Revenue"], color="#C1666B")
    axes[1].set_title("Top Products by Revenue")
    axes[1].set_xlabel("Revenue")
    fig.tight_layout()
    fig.savefig(figures_path / "top_products.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.bar(price_segments["PriceSegment"].astype(str), price_segments["Quantity"], color="#6C5B7B")
    ax.set_title("Purchased Quantity by Price Segment")
    ax.set_xlabel("Price segment based on UnitPrice quartiles")
    ax.set_ylabel("Quantity")
    fig.tight_layout()
    fig.savefig(figures_path / "price_segments.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.boxplot(order_values["OrderValue"], vert=False, showfliers=True)
    ax.set_xscale("log")
    ax.set_title("Order Value Distribution (Log Scale)")
    ax.set_xlabel("Order value")
    ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(figures_path / "order_value_boxplot.png", dpi=160)
    plt.close(fig)

    country_chart = country_revenue.head(10).sort_values("Revenue")
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(country_chart["Country"], country_chart["Revenue"], color="#4C78A8")
    ax.set_xscale("log")
    ax.set_title("Top Countries by Gross Revenue (Log Scale)")
    ax.set_xlabel("Revenue")
    fig.tight_layout()
    fig.savefig(figures_path / "country_revenue.png", dpi=160)
    plt.close(fig)

    peak_month = monthly_revenue.loc[monthly_revenue["Revenue"].idxmax()]
    top_quantity = top_products_quantity.iloc[0]
    top_revenue = top_products_revenue.iloc[0]
    leading_segment = price_segments.loc[price_segments["Quantity"].idxmax()]
    top_customer = top_customers.iloc[0]
    top_country = country_revenue.iloc[0]
    longest_inactive = inactive_customers.iloc[0]
    most_cancelled = cancelled_products.iloc[0]

    report_lines = [
        "# EDA Results",
        "",
        "Các kết quả dưới đây được tính từ `cleaned_retail.csv` và "
        "`customer_segments.csv`. Doanh thu sản phẩm, tháng và quốc gia chỉ dùng "
        "normal sales; cancellation được phân tích riêng.",
        "",
        "## 1. Doanh thu theo thời gian",
        "",
        f"Tháng có gross revenue cao nhất là `{peak_month['OrderMonth']}` với "
        f"{_currency(peak_month['Revenue'])}.",
        "",
        "## 2. Sản phẩm bán nhiều nhất",
        "",
        f"`{top_quantity['Description']}` (`{top_quantity['StockCode']}`) có tổng "
        f"Quantity cao nhất: {top_quantity['Quantity']:,.0f}.",
        "",
        "## 3. Sản phẩm tạo doanh thu cao nhất",
        "",
        f"`{top_revenue['Description']}` (`{top_revenue['StockCode']}`) đứng đầu "
        f"theo Revenue: {_currency(top_revenue['Revenue'])}. Kết quả giữ nguyên "
        "các mã phí/dịch vụ có trong dataset; chưa tự động loại chúng.",
        "",
        "## 4. Phân khúc giá có lượng mua cao nhất",
        "",
        f"Phân khúc `{leading_segment['PriceSegment']}` có Quantity cao nhất: "
        f"{leading_segment['Quantity']:,.0f}. Các phân khúc được xác định bằng "
        f"tứ phân vị UnitPrice: Q1={q1:.2f}, Median={median:.2f}, Q3={q3:.2f}.",
        "",
        "## 5. Khách hàng chi tiêu nhiều và mua thường xuyên",
        "",
        f"Trong nhóm Champions, CustomerID `{top_customer['CustomerID']:.0f}` có "
        f"Monetary cao nhất: {_currency(top_customer['Monetary'])}, Frequency="
        f"{top_customer['Frequency']:,.0f}.",
        "",
        "## 6. Quốc gia đóng góp doanh thu nhiều nhất",
        "",
        f"`{top_country['Country']}` có gross revenue cao nhất: "
        f"{_currency(top_country['Revenue'])}.",
        "",
        "## 7. Khách hàng lâu không quay lại",
        "",
        f"CustomerID `{longest_inactive['CustomerID']:.0f}` có Recency lớn nhất "
        f"trong nhóm Lost/At Risk: {longest_inactive['Recency']:,.0f} ngày.",
        "",
        "## 8. Sản phẩm thường xuất hiện trong đơn bị hủy",
        "",
        f"`{most_cancelled['Description']}` (`{most_cancelled['StockCode']}`) xuất "
        f"hiện trong {most_cancelled['CancelledInvoiceCount']:,.0f} cancellation "
        "invoices, cao nhất theo tiêu chí này.",
        "",
        "## Phạm vi",
        "",
        "EDA này không thêm dữ liệu ngoài dataset và không tự động xóa outlier, "
        "mã phí hoặc nghiệp vụ nội bộ. Các file chi tiết nằm trong "
        "`reports/tables/`; biểu đồ nằm trong `reports/figures/`.",
        "",
    ]
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    return {
        "monthly_revenue": monthly_revenue,
        "top_products_quantity": top_products_quantity,
        "top_products_revenue": top_products_revenue,
        "price_segments": price_segments,
        "top_customers": top_customers,
        "country_revenue": country_revenue,
        "inactive_customers": inactive_customers,
        "cancelled_products": cancelled_products,
        "order_values": order_values,
    }
