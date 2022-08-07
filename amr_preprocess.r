library('dplyr')
#library('xlsx') xlsx library require java runtime which I don't like
library(WriteXLS)

rm(list = ls())

#Loading csv file
chevrondata <- read.csv("outdata/ast_data_chevron_clean.csv", header=TRUE)

# Creating a grouped data to count R, I and S
OutputTable <- data.frame(
  OutputTable1 <- chevrondata %>%
    group_by(specimen_category, pathogen, antibiotic) %>%
    summarise(count_s = sum(result == 'S')),

  OutputTable2 <- chevrondata %>%
    group_by(specimen_category, pathogen, antibiotic) %>%
    summarise(count_i = sum(result == 'I')),

  OutputTable3 <- chevrondata %>%
    group_by(specimen_category, pathogen, antibiotic) %>%
    summarise(count_r = sum(result == 'R'))

)
# Cleaning the output table
FinalOutputTable = subset(OutputTable, select = -c(antibiotic.1, pathogen.1, specimen_category.1,
                                                   antibiotic.2, pathogen.2, specimen_category.2))

#Calculating Total count and adding them to a new column
FinalOutputTable$total = rowSums(FinalOutputTable[,c("count_s", "count_i", "count_r")])
# Calculating sensitivity as percentage of total count
FinalOutputTable$sensitivity <- FinalOutputTable$count_s/FinalOutputTable$total

write.csv(FinalOutputTable,'pre-processed.csv')
