import json, sys
from parser.parser import StatementParser
from dataclasses import asdict

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_parser.py <path_to_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    parser = StatementParser()
    result = parser.parse(pdf_path)
    result_dict = asdict(result)
    result_dict["transactions"] = [asdict(t) for t in result.transactions]

    output_path = "outputs/parsed_results.json"
    with open(output_path, "w") as f:
        json.dump(result_dict, f, indent=2)

    print(f"\n✅ Parsing completed! Output saved at: {output_path}\n")
    print(json.dumps(result_dict, indent=2))

if __name__ == "__main__":
    main()
