import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

# Define a dynamic schema
schema = avro.schema.parse('{"type": "record", "name": "Person", "fields": [{"name": "name", "type": "string"}, {"name": "age", "type": "int"}]}')

# Write data to a file
with open('data.avro', 'wb') as out:
    writer = DataFileWriter(out, DatumWriter(), schema)
    writer.append({"name": "Alice", "age": 25})
    writer.close()

# Read data from the file
with open('data.avro', 'rb') as fo:
    reader = DataFileReader(fo, DatumReader())
    for person in reader:        
        print(person)
