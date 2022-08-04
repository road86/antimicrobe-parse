#Loading csv file
chevrondata <- read.csv("C:\\Users\\5CG8104PKQ\\repo\\antimicrobe-parse\\outdata\\ast_data_chevron_clean.csv", header=TRUE)

# Creating a grouped data to count R, I and S
OutputTable <- data.frame(
  OutputTable1 <- chevrondata %>%
    group_by(specimen, pathogen, antibiotic) %>%
    summarise(Count_S = sum(result == 'S')),
  
  OutputTable2 <- chevrondata %>%
    group_by(specimen, pathogen, antibiotic) %>%
    summarise(Count_I = sum(result == 'I')),
  
  OutputTable3 <- chevrondata %>%
    group_by(specimen, pathogen, antibiotic) %>%
    summarise(Count_R = sum(result == 'R'))
  
)
# Cleaning the output table
FinalOutputTable = subset(OutputTable, select = -c(antibiotic.1, pathogen.1, specimen.1,
                                                   antibiotic.2, pathogen.2, specimen.2))

#Calculating Total count and adding them to a new column
FinalOutputTable$TotalCount = rowSums(FinalOutputTable[,c("Count_S", "Count_I", "Count_R")])
# Calculating sensitivity as percentage of total count
FinalOutputTable$SensistivityPercent <- FinalOutputTable$Count_S/FinalOutputTable$TotalCount


##Separating into Specimen-wise tables
# 1. Separating the Final Output Table into smaller tables according to "Specimen"
for(i in unique(FinalOutputTable$specimen)) {
  nam <- paste('FinalOutputTable', i, sep = ".")
  assign(nam, FinalOutputTable[FinalOutputTable$specimen==i,])
  
}

#Step 2. Creating a workbook with multiple tables

specimenwisetable <- list("Ascitic Fluid" = `FinalOutputTable.Ascitic Fluid`,
                          'Aural' = FinalOutputTable.Aural,
                          'Aural Swab' = `FinalOutputTable.Aural Swab`,
                          'Aural Sawb Left' = `FinalOutputTable.Aural Swab (Left)`,
                          "Blood" = FinalOutputTable.Blood,
                          "Breast" = FinalOutputTable.Breast,
                          "Bronchial Lavage" = `FinalOutputTable.Bronchial Lavage`,
                          "Catheter Tip" = `FinalOutputTable.Catheter tip.`,
                          "Cervical Discharge" = `FinalOutputTable.Cervical Discharge`,
                          "Conjunctival Swab" = `FinalOutputTable.Conjunctival Swab`,
                          "CSF" = FinalOutputTable.CSF,
                          "Deep Tracheal" = `FinalOutputTable.Deep Tracheal`,
                          "Deep Tracheal Swab" = `FinalOutputTable.Deep tracheal Swab`,
                          "Discharge" = FinalOutputTable.Discharge,
                          "Ear  Swab" = `FinalOutputTable.Ear  Swab`,
                          "Ear sw" = `FinalOutputTable.Ear swab`,
                          "Ea Swab" = `FinalOutputTable.Ear Swab`,
                          "E S." = `FinalOutputTable.Ear Swab.`,
                          "EndoTracheal Secretion" = `FinalOutputTable.Endotracheal Secretion`,
                          "ET-Tube Swab" = `FinalOutputTable.ET-Tube Swab`,
                          "ET-tube" = `FinalOutputTable.ET tube`,
                          "ET Tube" = `FinalOutputTable.ET Tube`,
                          "Eye A/C Fluid" = `FinalOutputTable.Eye A/C Fluid`,
                          "FinalOutputTable.Eye Fluid" = `FinalOutputTable.Eye Fluid`,
                          "High Vaginal Swab" = `FinalOutputTable.High Vaginal Swab`,
                          "HVS" = FinalOutputTable.HVS,
                          "Left Breast" = `FinalOutputTable.Left Breast`,
                          "Nipple discharge" = `FinalOutputTable.Nipple discharge`,
                          "Nipple Dis" = `FinalOutputTable.Nipple Discharge`,
                          "Oral swab" = `FinalOutputTable.Oral swab`,
                          "O S" = `FinalOutputTable.Oral Swab`,
                          "Parietal Abscess Fluid" = `FinalOutputTable.Parietal Abscess Fluid`,
                          "Pus" = FinalOutputTable.Pus,
                          "Pus (Left Knee)" = `FinalOutputTable.Pus (Left Knee)`,
                          "Rt Vit Fluid" = `FinalOutputTable.Rt. Vit Fluid`,
                          "semen" = FinalOutputTable.Semen,
                          "Sero Sanguinous Fluid" = `FinalOutputTable.Sero Sanguinous Fluid`,
                          "Sputum" = FinalOutputTable.Sputum,
                          "Stool" = FinalOutputTable.Stool,
                          "Subphrenic Fluid" =`FinalOutputTable.Subphrenic Fluid`,
                          "Swab" = FinalOutputTable.Swab,
                          "Swab from Rt Tibia" = `FinalOutputTable.Swab from Rt. Tibia for C/S.`,
                          "Synovial Fluid" = `FinalOutputTable.Synovial Fluid`,
                          "Throat Swab" = `FinalOutputTable.Throat Swab`,
                          "Throat Swab." = `FinalOutputTable.Throat Swab.`,
                          "Tracheal aspirate" = `FinalOutputTable.Tracheal aspirate`,
                          "Trach Asp" = `FinalOutputTable.Tracheal Aspirate`,
                          "Tracheal Swab" = `FinalOutputTable.Tracheal Swab`,
                          "Tracheostomy Swab" = `FinalOutputTable.Tracheostomy Swab`,
                          "Umbilical Swab" = `FinalOutputTable.Umbilical Swab`,
                          "Urethral Discharge" = `FinalOutputTable.Urethral Discharge`,
                          "Urethral Swab" = `FinalOutputTable.Urethral Swab`,
                          "Urine" = FinalOutputTable.Urine,
                          "Vaginal Swab" = `FinalOutputTable.Vaginal Swab`,
                          "Vit Fluid" = `FinalOutputTable.Vit Fluid`,
                          "Wound" = FinalOutputTable.Wound,
                          "W  S" = `FinalOutputTable.Wound  Swab`,
                          "Wound Discharge" = `FinalOutputTable.Wound Discharge`,
                          "w Swab" = `FinalOutputTable.wound Swab`,
                          "Wound Sw" = `FinalOutputTable.Wound Swab`
                          
)

# Export as xls file
write.xlsx(specimenwisetable, file = "C:\\Users\\5CG8104PKQ\\repo\\antimicrobe-parse\\outdata\\specimenwise.xls")
