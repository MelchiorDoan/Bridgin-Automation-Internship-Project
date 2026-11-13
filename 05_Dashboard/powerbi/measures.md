# Power BI parameter and measures

Check each formula against the model in Power BI before relying on this file. Table, column and measure names may differ.

## Model

- Tables: `fact_energyconsumption`, `fact_homeappliance`, `dim_home`, `dim_appliance` (created by the notebook in the parent folder).
- Relationships (one to many, single direction): `dim_home[home_id]` to `fact_energyconsumption[home_id]`, and `dim_home[home_id]` to `fact_homeappliance[home_id]`.

## Parameter

`Electricity rate`: what-if parameter, decimal, minimum 0.10, maximum 0.60, increment 0.01, default 0.33 ($ per kWh). It creates the measure `[Electricity rate Value]`.

## Base measures (typical definitions, confirm in the model)

    Avg kWh selected home = AVERAGE ( fact_energyconsumption[kwh] )

    Avg kWh all homes =
    CALCULATE ( AVERAGE ( fact_energyconsumption[kwh] ), REMOVEFILTERS ( dim_home ) )

## Cost page

    Avg cost selected = [Avg kWh selected home] * [Electricity rate Value]

    Avg cost all homes = [Avg kWh all homes] * [Electricity rate Value]

    Cost difference vs all homes =
    DIVIDE ( [Avg cost selected] - [Avg cost all homes], [Avg cost all homes] )

    Difference card =
    VAR selectedHomes = COUNTROWS ( VALUES ( dim_home[home_id] ) )
    VAR allHomes = CALCULATE ( COUNTROWS ( dim_home ), ALL ( dim_home ) )
    RETURN
        IF ( selectedHomes = allHomes, "N/A",
             FORMAT ( [Cost difference vs all homes], "+0.0%;-0.0%;0.0%" ) )

    Share of cost AC and Heater =
    VAR perAppliance =
        ADDCOLUMNS (
            VALUES ( fact_energyconsumption[appliance] ),
            "@kwh", CALCULATE ( AVERAGE ( fact_energyconsumption[kwh] ) )
        )
    RETURN
        DIVIDE (
            SUMX ( FILTER ( perAppliance, [appliance] IN { "Air Conditioning", "Heater" } ), [@kwh] ),
            SUMX ( perAppliance, [@kwh] )
        )

Calculated column on `dim_home` (used by the Top 10 chart):

    Home label = "Home " & dim_home[home_id]

## Household Profile page

    Diff vs all homes by appliance =
    DIVIDE ( [Avg kWh selected home] - [Avg kWh all homes], [Avg kWh all homes] )

    Rank by average kWh =
    VAR _home = SELECTEDVALUE ( dim_home[home_id] )
    RETURN
        IF ( NOT ISBLANK ( _home ),
             RANKX ( ALL ( dim_home ), dim_home[avg_kwh], MAX ( dim_home[avg_kwh] ), DESC, SKIP ) )

    Uses more than (card) =
    IF ( HASONEVALUE ( dim_home[home_id] ),
         FORMAT ( DIVIDE ( COUNTROWS ( ALL ( dim_home ) ) - [Rank by average kWh],
                           COUNTROWS ( ALL ( dim_home ) ) ), "0.0%" ) & " of homes",
         "Select one home" )

## Appliance Summary page

    Level =
    VAR _p = AVERAGE ( fact_homeappliance[percentile] )
    RETURN
        IF ( ISBLANK ( _p ), BLANK (),
             SWITCH ( TRUE (), _p >= 75, "High", _p >= 25, "Medium", "Low" ) )

    Appliances High = CALCULATE ( COUNTROWS ( fact_homeappliance ), fact_homeappliance[percentile] >= 75 )

    Appliances Medium =
    CALCULATE ( COUNTROWS ( fact_homeappliance ),
                fact_homeappliance[percentile] >= 25, fact_homeappliance[percentile] < 75 )

    Appliances Low = CALCULATE ( COUNTROWS ( fact_homeappliance ), fact_homeappliance[percentile] < 25 )
