class Rating:
  def __init__(self, raters, artists):
    self.raters = raters
    self.artists = artists


class Rater:
  def __init__(self, scores, comments):
    self.scores = scores
    self.comments = comments


class Artist:
  def __init__(self, songs, overallScore):
    self.songs = songs
    self.overallScore = overallScore