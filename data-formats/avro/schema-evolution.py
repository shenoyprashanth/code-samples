import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

# Define initial schema
schema_v1 = avro.schema.parse('{"type": "record", "name": "Person", "fields": [{"name": "name", "type": "string"}, {"name": "age", "type": "int"}]}')

# Write data to a file using the initial schema
with open('data_v1.avro', 'wb') as out:
    writer = DataFileWriter(out, DatumWriter(), schema_v1)
    writer.append({"name": "Alice", "age": 25})
    writer.close()

# Define new schema for version 2 of Person record
schema_v2 = avro.schema.parse('{"type": "record", "name": "Person", "fields": [{"name": "email", "type": ["null", "string"], "default": null}]}')

# Read data from the file using the new schema
with open('data_v1.avro', 'rb') as fo:
    reader = DataFileReader(fo, DatumReader())
    for person in reader:
        # Convert the old schema data to new schema data by adding the default value for new field
        person['email'] = None 
        print(type(person['age']))
        print(person)
