import filedate
import json
from dateutil import parser
from os.path import exists

input_file = open("../.input/input.json", "r")

input_data = json.load(input_file)

total_notes = 0

for item in input_data["items"]:
    if item["content_type"] == "Note":
        duplicate_counter = 1

        filename = f"output/{item['content']['title'].replace('/', '-')}.md"

        while exists(filename):
            trimer = 3
            if duplicate_counter > 1:
                trimer = 5
            filename = f"{filename[:-trimer]}-{duplicate_counter}.md"
            duplicate_counter = duplicate_counter + 1

        file = open(filename, "w+")

        created_at = parser.parse(item["created_at"])
        updated_at = parser.parse(item["updated_at"])

        file.write(
            f"---\ndate: {created_at.strftime('%Y-%m-%d')}\naliases: []\n---\n\n{item['content']['text']}"
        )

        file.close()

        a_file = filedate.File(filename)

        a_file.set(
            created=created_at.strftime("%Y.%m.%d %H:%M:%S"),
            modified=updated_at.strftime("%Y.%m.%d %H:%M:%S"),
        )

        total_notes = total_notes + 1

print(total_notes)
