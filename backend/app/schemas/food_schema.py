food_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "code": {"type": "string"},
        "name": {"type": "string"},
        "brands": {"type": "string"},
        "serving_quantity": {"type": "integer"},
        "unit": {"type": "string"},
        "raw": {"type": "boolean"},
        "energy_serving": {"type": "integer"},
        "energy_100g": {"type": "integer"},
        "fiber_serving": {"type": "number"},
        "fiber_100g": {"type": "number"},
        "salt_serving": {"type": "number"},
        "salt_100g": {"type": "number"},
        "carbohydrates_100g": {"type": "number"},
        "carbohydrates_serving": {"type": "number"},
        "fat_100g": {"type": "number"},
        "fat_serving": {"type": "number"},
        "proteins_100g": {"type": "number"},
        "proteins_serving": {"type": "number"},
    },
    "required": ["code", "name"],  # Specify required fields here
}
