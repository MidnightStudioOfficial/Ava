# c1 = "That is nice to hear I am glad you are."
# c2 = "That is good to hear I am happy you are."
c1 = "That is nice to hear I am glad you are."
c2 = "That is good to hear and I am happy that you are."

g1 = TopicModeling()
print("TopicModeling:"+str(g1.compare(c1, c2)))
g2 = TopicAndCosineSimilarity()
print("TopicAndCosineSimilarity:"+str(g2.compare(c1, c2)))
g6 = TopicAndCosineSimilarity2()
print("TopicAndCosineSimilarity2:"+str(g6.compare(c1, c2)))
g3 = CosineSimilarity()
print("CosineSimilarity:"+str(g3.compare(c1, c2)))
g5 = LevenshteinDistance()
print("LevenshteinDistance:"+str(g5.compare(c1, c2)))
g4 = avrig()
print(g4.compare(c1, c2))
