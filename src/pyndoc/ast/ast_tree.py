from collections import UserList


class ASTTree(UserList):
    def __str__(self) -> str:
        blocks_str = "\n".join(["  " + str(block).replace("\n", "\n  ") + "," for block in self.data])
        return blocks_str
