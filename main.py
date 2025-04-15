from services.batch_processor import BatchProcessor

if __name__ == "__main__":
    processor = BatchProcessor()
    processor.process_from_file("input_data.json")