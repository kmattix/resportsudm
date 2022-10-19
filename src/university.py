#Object that represents and entry in the Esports Program Master List.

class University:
    universities = {}

    def __init__(self, row: list):
        for ignored in range(len(row) - 1, 16): #pad the entry if it's missing fields
            row.append('')

        self.name = self.__check(row[0])
        self.acronym = self.__check(row[1])
        self.assoc_name = self.__check(row[2])
        self.state = self.__check(row[3])
        self.logo = self.__check(row[4])
        self.logo2 = self.__check(row[5])
        self.misc = self.__check(row[6])
        self.primarycolor = self.__check(row[7])
        self.secondarycolor = self.__check(row[8])
        self.discord = self.__check(row[9])
        self.twitter = self.__check(row[10])
        self.twitch = self.__check(row[11])
        self.youtube = self.__check(row[12])
        self.facebook = self.__check(row[13])
        self.instagram = self.__check(row[14])
        self.tiktok = self.__check(row[15])
        self.website = self.__check(row[16])

    def __check(self, s: str) -> str:
        return 'N/A' if s == '' or\
                        s.isspace() or\
                        s.lower().strip() == 'missing' else s.strip()

    def __str__(self) -> str:
        return f"{self.name} [{self.acronym}], {self.state}\n"\
        f"logo={self.logo}\n"\
        f"logo2={self.logo2}\n"\
        f"misc={self.misc}\n"\
        f"primary={self.primarycolor} secondary={self.secondarycolor}\n"\
        f"discord={self.discord}\n"\
        f"twitter={self.twitter}\n"\
        f"twitch={self.twitch}\n"\
        f"youtube={self.youtube}\n"\
        f"facebook={self.facebook}\n"\
        f"instagram={self.instagram}\n"\
        f"tiktok={self.tiktok}\n"\
        f"website={self.website}"