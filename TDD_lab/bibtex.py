

def extract_author(author_str):
    author_str = author_str.strip()

    if ',' in author_str:
        parts = author_str.split(',') #split at coma
        if len(parts) ==2:
            surname = parts[0].strip()
            forenames = parts[1].strip()
            return (surname, forenames)

    parts = author_str.split()
    #if only one part = surname
    if len(parts) == 1:
        return parts[0], ''

    surname = parts[-1] # last is always the surname
    forenames = " ".join(parts[:-1])
    return surname, forenames

def extract_authors(authors_str):
    authors = authors_str.split(" and ")

    return [extract_author(author.strip()) for author in authors]
