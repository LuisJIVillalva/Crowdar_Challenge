
DEPARTMENTS_SCHEMA = {
    "type": "object",
    "required": ["departments", "landings", "more_categories", "high_priority"],
    "properties": {

        "departments": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["name", "categories"],
                "properties": {
                    "name": {"type": "string"},
                    "categories": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "required": ["id", "permalink"],
                            "properties": {
                                "id":        {"type": "string"},
                                "name":      {"type": "string"},
                                "permalink": {"type": "string"},
                                "children_categories": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "required": ["id", "permalink"],
                                        "properties": {
                                            "id":        {"type": "string"},
                                            "name":      {"type": "string"},
                                            "permalink": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },

        "landings": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["label", "permalink"],
                "properties": {
                    "label":     {"type": "string"},
                    "permalink": {"type": "string"}
                }
            }
        },

        "more_categories": {
            "type": "object",
            "required": ["label", "permalink"],
            "properties": {
                "label":     {"type": "string"},
                "permalink": {"type": "string"}
            }
        },

        "high_priority": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["label", "permalink"],
                "properties": {
                    "label":     {"type": "string"},
                    "permalink": {"type": "string"}
                }
            }
        }
    }
}

