# https://juliasilge.com/blog/sherlock-holmes-stm/


# install.packages("stm")
library(stm)
library(tidyverse)
library(gutenbergr)
library(dplyr)
library(tidytext)
library(quanteda)
# library(rjson)
library(tm)

setwd("/Users/admin/Desktop/NLP-win-21/jason")
data <- read.csv("/Users/admin/Desktop/NLP-data/sample_df-V1.csv") 
n_docs <- length(data[[2]]) 
n_topic <- 10


# PREP 
processed <- textProcessor(data$text, metadata = data) 
out <- prepDocuments(processed$documents, processed$vocab, processed$meta, 
                     lower.thresh = 2, upper.thresh = as.integer(n_docs / 2))
docs <- out$documents 
# vocab <- out$vocab 
meta <-out$meta 

# Estimate STM 
stm1 <- stm(documents = out$documents, vocab = out$vocab,
             K = n_topic, prevalence =~ s(date), 
             max.em.its = 20, data = out$meta,
             init.type = "Spectral")
# mu <- stm1$mu
# sigma <- stm1$sigma 
print(stm1$time)
vocab <- stm1$vocab

# 找每个topic的words -- top 10 words
n_big_idx <- function(x, n=3) {
  nx <- length(x)
  p <- nx-n
  xp <- sort(x, partial=p)[p]
  which(x > xp)}
beta <- stm1$beta # log word prob in each topic 
topic_word <- beta$logbeta[[1]]

topic_names = c(1:n_topic)
names(topic_names) = c(1:n_topic)
for (i in c(1:n_topic)) {
  print(i)
  topic_names[i] = paste(vocab[n_big_idx(topic_word[i,], n=10)],
                         collapse = ' ')
}

topic_names <- list(topic_names)
library(data.table)
setDT(topic_names)
fwrite(list(topic_names[[1]]), file = "topic_names-test1")

# 找每个document的topic 
vocab <- stm1$vocab 
theta <- stm1$theta # document-topic matrix 
doc_topic <- theta
prob_lim <- .6 
thres <- .01 

# doc_topic[1,] 
doc_topic_out <- add_column(tibble(doc_topic), meta$date) 
write.table(doc_topic_out , file = "doc_topic-test1.csv")


# doc_i <- doc_topic[i,] 
# doc_i[doc_i > thres] 
# meta$topic <- 0
# for (i in c(1:n_topic)){
#  pass  
# }
# sum(doc_i[n_big_idx(doc_i, 4)])




## # # # # #  ## # # # # # ## # # # # # ## # # # # # ## # # # # # ## # # # # # 
# Sanity check 
# i is the index of document 
i <- 100
i_str <-  as.character(i)
paste(vocab[docs[i][[i_str]][1,]], collapse = ' ') # 第i个document 

i_topic_idx <- n_big_idx(doc_topic[i,], 1)


paste(vocab[n_big_idx(topic_word[i_topic_idx,], n=10)],
      collapse = ' ')

