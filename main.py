"""Entry point chạy lại toàn bộ phần pipeline đã được triển khai."""

from pathlib import Path

from src.build_web import build_web, export_web_tables
from src.eda_analysis import run_eda
from src.outlier_analysis import analyze_outliers
from src.retail_data_processor import RetailDataProcessor
from src.validation import validate_results


PROJECT_ROOT = Path(__file__).resolve().parent
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "Online_Retail.xlsx"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def main() -> tuple[RetailDataProcessor, dict, dict]:
    """Chạy pipeline dùng chung cho CLI và notebook."""
    processor = RetailDataProcessor(RAW_FILE)
    processor.load_data()
    processor.clean_data()

    invoice_records, country_summary, product_codes, date_range = (
        processor.create_basic_structures()
    )
    print("Date range:", date_range)
    print("Number of unique products:", len(product_codes))
    print("Country summary sample:", list(country_summary.items())[:5])
    print("Invoice records sample:", invoice_records[:2])

    segments = processor.create_customer_segments()
    print("Customer segment distribution:")
    print(segments["Segment"].value_counts())

    cleaned_file = PROCESSED_DIR / "cleaned_retail.csv"
    customer_file = PROCESSED_DIR / "customer_segments.csv"
    processor.export_results(
        cleaned_file=cleaned_file,
        customer_file=customer_file,
        customer_segments=segments,
    )

    checks = validate_results(cleaned_file, customer_file)
    failures = {name: count for name, count in checks.items() if count}
    if failures:
        raise ValueError(f"Validation failed; EDA and dashboard were not rebuilt: {failures}")

    analyze_outliers(
        input_file=cleaned_file,
        summary_file=PROCESSED_DIR / "outlier_summary.csv",
        outlier_file=PROCESSED_DIR / "outliers_detected.csv",
    )
    tables = run_eda(
        cleaned_file=cleaned_file,
        customer_file=customer_file,
        tables_dir=PROJECT_ROOT / "reports" / "tables",
        figures_dir=PROJECT_ROOT / "reports" / "figures",
        report_file=PROJECT_ROOT / "reports" / "eda_results.md",
    )
    export_web_tables(cleaned_file, customer_file)
    dashboard = build_web(
        expected_net=processor.df["Revenue"].sum(),
        expected_customers=len(segments),
    )
    print("EDA and dashboard exported.")
    return processor, tables, dashboard


if __name__ == "__main__":
    main()

