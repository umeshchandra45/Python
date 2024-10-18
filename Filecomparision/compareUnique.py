import re

# Main function,
def main():
    input_char_seq = "In this world, the word of mouth is what matters"
    options = re.compile(r"world|word|mouth|matters")
    matches = options.findall(input_char_seq)

    for match in matches:
        print(f"Found {match}.")
    match_list = list(matches)
    print("list:", match_list)

    match_result = bool(re.search(r"par", "comparision"))
    print(match_result)


if __name__ == "__main__":
    main()