"""Entry point chạy lại toàn bộ phần pipeline đã được triển khai."""

from pathlib import Path

from src.eda_analysis import run_eda
from src.outlier_analysis import analyze_outliers
from src.retail_data_processor import RetailDataProcessor
from src.validation import validate_results


PROJECT_ROOT = Path(__file__).resolve().parent
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "Online_Retail.xlsx"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def main() -> None:
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

    monthly, country, product = processor.analyze_revenue()
    print("Revenue by month:")
    print(monthly)
    print("Top countries:")
    print(country.head())
    print("Top products:")
    print(product.head())

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

    analyze_outliers(
        input_file=cleaned_file,
        summary_file=PROCESSED_DIR / "outlier_summary.csv",
        outlier_file=PROCESSED_DIR / "outliers_detected.csv",
    )
    validate_results(cleaned_file, customer_file)
    run_eda(
        cleaned_file=cleaned_file,
        customer_file=customer_file,
        tables_dir=PROJECT_ROOT / "reports" / "tables",
        figures_dir=PROJECT_ROOT / "reports" / "figures",
        report_file=PROJECT_ROOT / "reports" / "eda_results.md",
    )


if __name__ == "__main__":
    main()

