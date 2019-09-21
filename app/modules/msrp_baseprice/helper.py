import mongoengine

def mongo_to_dict(obj, exclude_fields):
	return_data = []

	if obj is None:
		return None

	if isinstance(obj, mongoengine.Document):
		return_data.append(("id",str(obj.id)))

	for field_name in obj._fields:

		if field_name in exclude_fields:
			continue

		if field_name in ("id",):
			continue

		data = obj._data[field_name]

		if isinstance(obj._fields[field_name], mongoengine.ListField):
			return_data.append((field_name, list_field_to_dict(data)))
		elif isinstance(obj._fields[field_name], mongoengine.EmbeddedDocumentField):
			return_data.append((field_name, mongo_to_dict(data,[])))
		elif isinstance(obj._fields[field_name], mongoengine.DictField):
			return_data.append((field_name, data))
		else:
			return_data.append((field_name, mongo_to_python_type(obj._fields[field_name],data)))

	return dict(return_data)

def list_field_to_dict(list_field):

	return_data = []

	for item in list_field:
		if isinstance(item, mongoengine.EmbeddedDocument):
			return_data.append(mongo_to_dict(item,[]))
		else:
			return_data.append(mongo_to_python_type(item,item))


	return return_data

def mongo_to_python_type(field,data):

	if isinstance(field, mongoengine.DateTimeField):
		return str(data.isoformat())
	elif isinstance(field, mongoengine.ComplexDateTimeField):
		return field.to_python(data).isoformat()
	elif isinstance(field, mongoengine.StringField):
		return str(data)
	elif isinstance(field, mongoengine.FloatField):
		return float(data)
	elif isinstance(field, mongoengine.IntField):
		return int(data)
	elif isinstance(field, mongoengine.BooleanField):
		return bool(data)
	elif isinstance(field, mongoengine.ObjectIdField):
		return str(data)
	elif isinstance(field, mongoengine.DecimalField):
		return data
	else:
		return str(data)