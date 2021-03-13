# https://juliasilge.com/blog/sherlock-holmes-stm/


# install.packages("stm")
library(stm)
library(tidyverse)
library(gutenbergr)
library(dplyr)
library(tidytext)
library(quanteda)
library(tm)
library(data.table)
library("rjson")

setwd("/Users/admin/Desktop/NLP-win-21/jason") # working directory
# data <- read.csv("/Users/admin/Desktop/NLP-data/sample_df-V1.csv") # input data

data <- data.frame()
filepath <- "/Users/admin/Desktop/NLP-data/RMRB_5_each_month.jsonlist.json"

con = file(filepath, "r")
while ( TRUE ) {
  line = readLines(con, n = 1)
  if ( length(line) == 0 ) {
    break
  }
  json_data <- fromJSON(line)
  json_data <- data.frame(json_data)
  data <- rbind(data, json_data)
}
close(con)


trial_postfix <- "-test1.csv" # 输出两个文件的后缀
n_topic <- 50 
output_dir <- '' # output directory name 

n_docs <- length(data[[2]])  





# PREP 
processed <- textProcessor(data$text, metadata = data) 
out <- prepDocuments(processed$documents, processed$vocab, processed$meta, 
                     lower.thresh = 5, upper.thresh = as.integer(n_docs / 2))
docs <- out$documents 
n_docs <- length(docs)  

# vocab <- out$vocab 
meta <-out$meta 

# Estimate STM 
stm1 <- stm(documents = out$documents, vocab = out$vocab,
             K = n_topic, prevalence =~ s(date), 
             max.em.its = 20, data = out$meta,
             init.type = "Spectral")
# mu <- stm1$mu
# sigma <- stm1$sigma 
print("time used in topic modelling")
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
  # print(i)
  topic_names[i] = paste(vocab[n_big_idx(topic_word[i,], n=n_topic)],
                         collapse = ' ')
}

topic_names <- list(topic_names)
setDT(topic_names)
fwrite(list(topic_names[[1]]), 
       file = file.path(output_dir, paste("topic_names", trial_postfix)))

# 找每个document的topic 
vocab <- stm1$vocab 
theta <- stm1$theta # document-topic matrix 
doc_topic <- theta
prob_lim <- .6 
thres <- .01 

# doc_topic[1,] 
doc_topic_out <- add_column(tibble(doc_topic), meta$date) 
write.table(doc_topic_out , 
            file = file.path(output_dir, paste("doc_topic", trial_postfix)) )


# doc_i <- doc_topic[i,] 
# doc_i[doc_i > thres] 
# meta$topic <- 0
# for (i in c(1:n_topic)){
#  pass  
# }
# sum(doc_i[n_big_idx(doc_i, 4)])




## # # # # #  ## # # # # # ## # # # # # ## # # # # # ## # # # # # ## # # # # # 
# # Sanity check 
# # i is the index of document 
# i <- 100
# i_str <-  as.character(i)
# paste(vocab[docs[i][[i_str]][1,]], collapse = ' ') # 第i个document 
# 
# i_topic_idx <- n_big_idx(doc_topic[i,], 1)
# 
# 
# paste(vocab[n_big_idx(topic_word[i_topic_idx,], n=10)],
#       collapse = ' ')

