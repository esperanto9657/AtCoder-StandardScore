import getopt
import sys
import serialization

def calculate_standard_score(rating, options, birthyear_offset = 1, participation_offset = 1):
    df = serialization.load_data()
    for (k, v) in options.items():
        if k == "Country":
            df = df[df[k] == options[k]]
        if k == "Birthyear":
            df = df.dropna()
            df["Birthyear"] = df["Birthyear"].astype(int)
            df = df[(df[k] >= options[k] - birthyear_offset) & (df[k] <= options[k] + birthyear_offset)]
        if k == "Participation":
            df = df[(df[k] >= options[k] - participation_offset) & (df[k] <= options[k] + participation_offset)]

    df_rating = df["Rating"]
    standard_score = 10 * (rating - df_rating.mean()) / df_rating.std() + 50
    return standard_score

def main():
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], "c:b:p:")
    except getopt.GetoptError:
        print("usage: %s [-c country] [-b birthyear] [-p participation] [rating]" % sys.argv[0])
        
    option_dict = {}
    for (k, v) in opts:
        if k == "-c":
            option_dict["Country"] = v
        elif k == "-b":
            option_dict["Birthyear"] = int(v)
        elif k == "-p":
            option_dict["Participation"] = int(v)
    print(calculate_standard_score(int(args[0]), option_dict))

if __name__ == "__main__":
    main()