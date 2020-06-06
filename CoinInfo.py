class CoinInfo:
    Name = "",
    Value = "",
    YearsOfIssue = "",
    Description = "",
    SmallImgLoc = "",
    LargeImgLoc = ""

    def __init__(self, name, value, yearsOfIssue, description, smallImgLoc, largeImgLoc):
        self.Name = name
        self.Value = value
        self.YearsOfIssue = yearsOfIssue
        self.Description = description
        self.SmallImgLoc = smallImgLoc
        self.LargeImgLoc = largeImgLoc