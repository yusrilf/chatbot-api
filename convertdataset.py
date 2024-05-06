import csv
import json

def convert_csv_to_json(input_file, output_file):
    data = []
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        next(csvreader)  # Skip header
        for row in csvreader:
            question, answer = row
            data.append({"input": question.strip(), "output": answer.strip()})
    
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        for item in data:
            jsonfile.write(json.dumps(item) + '\n')

# Menggunakan fungsi untuk mengonversi dataset
input_csv_file = "qna_komcad_terbaru.csv"  # Ubah sesuai dengan nama file CSV Anda
output_json_file = "dataset_train.jsonl"  # Ubah sesuai dengan nama file JSON yang ingin Anda hasilkan
convert_csv_to_json(input_csv_file, output_json_file)
