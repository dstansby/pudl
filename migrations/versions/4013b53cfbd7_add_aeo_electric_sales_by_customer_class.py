"""Add AEO electric sales by customer class

Revision ID: 4013b53cfbd7
Revises: 53aababa3b9d
Create Date: 2024-05-06 10:51:58.749103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4013b53cfbd7'
down_revision = '1c7536e23a27'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('core_eiaaeo__yearly_projected_electric_sales',
    sa.Column('report_year', sa.Integer(), nullable=False, comment='Four-digit year in which the data was reported.'),
    sa.Column('electricity_market_module_region_eiaaeo', sa.Enum('florida_reliability_coordinating_council', 'midcontinent_central', 'midcontinent_east', 'midcontinent_south', 'midcontinent_west', 'northeast_power_coordinating_council_new_england', 'northeast_power_coordinating_council_new_york_city_and_long_island', 'northeast_power_coordinating_council_upstate_new_york', 'pjm_commonwealth_edison', 'pjm_dominion', 'pjm_east', 'pjm_west', 'serc_reliability_corporation_central', 'serc_reliability_corporation_east', 'serc_reliability_corporation_southeastern', 'southwest_power_pool_central', 'southwest_power_pool_north', 'southwest_power_pool_south', 'texas_reliability_entity', 'united_states', 'western_electricity_coordinating_council_basin', 'western_electricity_coordinating_council_california_north', 'western_electricity_coordinating_council_california_south', 'western_electricity_coordinating_council_northwest_power_pool_area', 'western_electricity_coordinating_council_rockies', 'western_electricity_coordinating_council_southwest'), nullable=False, comment='AEO projection region.'),
    sa.Column('model_case_eiaaeo', sa.Enum('aeo2022', 'high_economic_growth', 'high_macro_and_high_zero_carbon_technology_cost', 'high_macro_and_low_zero_carbon_technology_cost', 'high_oil_and_gas_supply', 'high_oil_price', 'high_uptake_of_inflation_reduction_act', 'high_zero_carbon_technology_cost', 'low_economic_growth', 'low_macro_and_high_zero_carbon_technology_cost', 'low_macro_and_low_zero_carbon_technology_cost', 'low_oil_and_gas_supply', 'low_oil_price', 'low_uptake_of_inflation_reduction_act', 'low_zero_carbon_technology_cost', 'no_inflation_reduction_act', 'reference'), nullable=False, comment='Factors such as economic growth, future oil prices, the ultimate size of domestic energy resources, and technological change are often uncertain. To illustrate some of these uncertainties, EIA runs side cases to show how the model responds to changes in key input variables compared with the Reference case. See https://www.eia.gov/outlooks/aeo/assumptions/case_descriptions.php for more details.'),
    sa.Column('projection_year', sa.Integer(), nullable=False, comment='The year of the projected value.'),
    sa.Column('customer_class', sa.Enum('commercial', 'industrial', 'direct_connection', 'other', 'residential', 'total', 'transportation'), nullable=False, comment="High level categorization of customer type: ['commercial', 'industrial', 'direct_connection', 'other', 'residential', 'total', 'transportation']."),
    sa.Column('sales_mwh', sa.Float(), nullable=True, comment='Quantity of electricity sold in MWh.'),
    sa.PrimaryKeyConstraint('report_year', 'electricity_market_module_region_eiaaeo', 'model_case_eiaaeo', 'projection_year', 'customer_class', name=op.f('pk_core_eiaaeo__yearly_projected_electric_sales'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('core_eiaaeo__yearly_projected_electric_sales')
    # ### end Alembic commands ###