# https://juliasilge.com/blog/sherlock-holmes-stm/


# install.packages("stm")
library(stm)
library(tidyverse)
library(gutenbergr)
library(dplyr)

sherlock_raw <- gutenberg_download(1661)

sherlock <- sherlock_raw %>%
  mutate(story = ifelse(str_detect(text, "ADVENTURE"),
                        text,
                        NA)) %>%
  fill(story) %>%
  filter(story != "THE ADVENTURES OF SHERLOCK HOLMES") %>%
  mutate(story = factor(story, levels = unique(story)))

sherlock


library(tidytext)
# transform the text data into a tidy data structure 
# also incorporate stop words (remove words that are not meaningful)

tidy_sherlock <- sherlock %>%
  mutate(line = row_number()) %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words) %>%
  filter(word != "holmes")
tidy_sherlock %>%
  count(word, sort = TRUE)

library(quanteda)
library(stm)

sherlock_dfm <- tidy_sherlock %>%
  count(story, word, sort = TRUE) %>%
  cast_dfm(story, word, n)

sherlock_sparse <- tidy_sherlock %>%
  count(story, word, sort = TRUE) %>%
  cast_sparse(story, word, n)

topic_model <- stm(sherlock_dfm, K = 6, 
                   verbose = FALSE, init.type = "Spectral")

td_beta <- tidy(topic_model) # normalize output as probability


td_beta %>%
  group_by(topic) %>%
  top_n(10, beta) %>%
  ungroup() %>%
  mutate(topic = paste0("Topic ", topic),
         term = reorder_within(term, beta, topic)) %>%
  ggplot(aes(term, beta, fill = as.factor(topic))) +
  geom_col(alpha = 0.8, show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free_y") +
  coord_flip() +
  scale_x_reordered() +
  labs(x = NULL, y = expression(beta),
       title = "Highest word probabilities for each topic",
       subtitle = "Different words are associated with different topics")

td_gamma <- tidy(topic_model, matrix = "gamma",                    
                 document_names = rownames(sherlock_dfm))

ggplot(td_gamma, aes(gamma, fill = as.factor(topic))) +
  geom_histogram(alpha = 0.8, show.legend = FALSE) +
  facet_wrap(~ topic, ncol = 3) +
  labs(title = "Distribution of document probabilities for each topic",
       subtitle = "Each topic is associated with 1-3 stories",
       y = "Number of stories", x = expression(gamma))




