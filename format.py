import json

def transform_annotations(data):
    result = {"paragraphs": []}

    annotations = {item["id"]: item for item in data[0]["annotations"][0]["result"] if "id" in item}

    # print("Annotations Dictionary:")
    # for key, value in annotations.items():
        # print(f"ID: {key}, Type: {value.get('from_name')}")

    def get_box(value, original_width, original_height, image_rotation):
        return {
            "x1": value["x"],
            "y1": value["y"],
            "x2": value["x"] + value["width"],
            "y2": value["y"] + value["height"],
            "rotation": value.get("rotation", 0),
            "original_width": original_width,
            "original_height": original_height,
            "image_rotation": image_rotation
        }

    for item in data[0]["annotations"][0]["result"]:
        if item.get("from_name") == "label" and "Paragraph" in item["value"]["labels"]:
            original_width = item["original_width"]
            original_height = item["original_height"]
            image_rotation = item["image_rotation"]

            paragraph = {
                "id": item["id"],
                "content": None,
                "box": get_box(item["value"], original_width, original_height, image_rotation),
                "words": []
            }
    
            # print(f"Processing Paragraph: {item['id']}")

            for trans in data[0]["annotations"][0]["result"]:
                if trans.get("from_name") == "transcription" and trans["id"] == item["id"]:
                    paragraph["content"] = trans["value"]["text"][0]
            # print(f"Paragraph Content: {paragraph['content']}")

            for word_item in data[0]["annotations"][0]["result"]:
                if word_item.get("parentID") == item["id"] and word_item.get("from_name") == "label" and "Word" in word_item["value"]["labels"]:
                    word = {
                        "id": word_item["id"],
                        "content": None,
                        "box": get_box(word_item["value"], original_width, original_height, image_rotation),
                        "characters": []
                    }
            
                    # print(f"Processing Word: {word_item['id']}")
            
                    for trans in data[0]["annotations"][0]["result"]:
                        if trans.get("from_name") == "transcription" and trans["id"] == word_item["id"]:
                            word["content"] = trans["value"]["text"][0]
            
                    # print(f"Word Content: {word['content']}")
            
                    for char_item in data[0]["annotations"][0]["result"]:
                        if char_item.get("parentID") == word_item["id"] and char_item.get("from_name") == "label" and "Character" in char_item["value"]["labels"]:
                            char = {
                                "id": char_item["id"],
                                "content": None,
                                "box": get_box(char_item["value"], original_width, original_height, image_rotation)
                            }
                    
                            # print(f"Processing Character: {char_item['id']}")
                    
                            for trans in data[0]["annotations"][0]["result"]:
                                if trans.get("from_name") == "transcription" and trans["id"] == char_item["id"]:
                                    char["content"] = trans["value"]["text"][0]
                    
                            # print(f"Character Content: {char['content']}")
                            word["characters"].append(char)
            
                    paragraph["words"].append(word)
    
            result["paragraphs"].append(paragraph)
    
    return result
with open("eg.json", "r") as f:
    data = json.load(f)
transformed_data = transform_annotations(data)
with open("output.json", "w") as f:
    json.dump(transformed_data, f, indent=4)

print("Transformed data saved to output.json")