import Data.List -- for foldl' which should be used instead of foldl
-- data to represent the directions.
-- I converted the input to capitalized directions so that Haskell can
-- automatically read them as movements.
data Movement = Forward Int | Up Int | Down Int
    deriving (Read, Show)

-- type alias to represent the submarine's position. Trying to juggle two
-- separate states is asking for trouble.
type X = Int
type Y = Int
type Aim = Int
type Position = (X, Y, Aim)

-- This is about as self explanatory as it gets hehe.
-- This is for part 1, so we ignore the aim.
applySimpleMove :: Position -> Movement -> Position
applySimpleMove (x, y, _) (Forward d) = (x + d, y, 0)
applySimpleMove (x, y, _) (Down d) = (x, y + d, 0)
applySimpleMove (x, y, _) (Up d) = (x, y - d, 0)

-- for part 2
applyComplicatedMove :: Position -> Movement -> Position
applyComplicatedMove (x, y, aim) (Forward d) = (x + d, y + d * aim, aim)
applyComplicatedMove (x, y, aim) (Down d) = (x, y, aim + d)
applyComplicatedMove (x, y, aim) (Up d) = (x, y, aim - d)

-- multiply the two values of a position together
mulPosition :: Position -> Int
mulPosition (x, y, _) = x * y

-- solution to part 1
solve1 :: [Movement] -> Int
-- like functools.reduce() in Python; applies over a list and accumulates
solve1 movements = mulPosition $ foldl' applySimpleMove startPos movements
    where startPos = (0, 0, 0)
-- solution to part 2
solve2 :: [Movement] -> Int
solve2 movements = mulPosition $ foldl' applyComplicatedMove startPos movements
    where startPos = (0, 0, 0)

main :: IO()
main = do
    content <- readFile "input.txt"
    -- interpret each line of the input as a Movement type
    let movements = [read ln :: Movement | ln <- lines content]
    print $ solve1 movements
    print $ solve2 movements