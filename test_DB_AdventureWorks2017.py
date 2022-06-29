import pandas
import pyodbc

import variables


class TestDataBase:
    conn = pyodbc.connect(DRIVER='{SQL Server}',
                          SERVER=variables.server_name,
                          DATABASE=variables.database_name,
                          Trusted_Connection='yes')

    def get_dataframe(self, query):
        print(query)
        df = pandas.read_sql_query(query, self.conn)
        return df

    def test_check_count_rows_in_address(self):
        """Check the count of rows in the table Person.Address table"""
        expected_res = 19614  # count of rows in the table
        df = self.get_dataframe("""
                                    SELECT *
                                    FROM [Person].[Address];
                                """)
        actual_df = df.shape[0]
        assert actual_df == expected_res, "The count of rows is different"

    def test_validity_verify_columns_count_in_document(self):
        """Check the count of columns in the Production.Document table"""
        expected_res = 14  # count of columns in the table
        df = self.get_dataframe("""
                                    SELECT *
                                    FROM INFORMATION_SCHEMA.COLUMNS;
                                """)
        actual_df = df[(df['TABLE_CATALOG'] == 'AdventureWorks2017')
                       & (df['TABLE_NAME'] == 'Document')]
        actual_df = actual_df.shape[0]
        assert actual_df == expected_res, "The count of columns does not match"

    def test_uniqueness_check_duplicates_in_unitMeasure(self):
        """Check the UnitMeasureCode field for duplicates
            in the Production.UnitMeasure table"""
        expected_res = 0  # there should be no duplicates
        df = self.get_dataframe("""
                                   SELECT *
                                   FROM [Production].[UnitMeasure];
                                """)
        actual_df = df[['UnitMeasureCode', 'Name']]. \
            groupby(['UnitMeasureCode']). \
            size().reset_index(name='counts')
        actual_df = actual_df[actual_df['counts'] > 1]
        actual_df = len(actual_df.index)
        assert actual_df == expected_res, "There are duplicates in the table"

    def test_validity_verify_column_name_data_type_in_unitMeasure(self):
        """Check the column name and data type
            in the Production.UnitMeasure table"""
        expected_res = [['UnitMeasureCode', 'nchar 3'],
                        ['Name', 'nvarchar 50'],
                        ['ModifiedDate', 'datetime']]
        df = self.get_dataframe("""
            SELECT COLUMN_NAME
                  ,TABLE_CATALOG
                  ,TABLE_NAME
                  ,CASE
                        WHEN CHARACTER_MAXIMUM_LENGTH is NULL
                        THEN Data_type
                        ELSE CONCAT (DATA_TYPE,' ',CHARACTER_MAXIMUM_LENGTH)
                        END [Data_type]
            FROM INFORMATION_SCHEMA.COLUMNS;
                                """)
        actual_df = df[['COLUMN_NAME', 'Data_type']]
        actual_df = actual_df[(df['TABLE_CATALOG'] == 'AdventureWorks2017')
                              & (df['TABLE_NAME'] == 'UnitMeasure')]
        actual_df = actual_df.values.tolist()
        assert actual_df == expected_res, \
            "The data type or column names are incorrect"

    def test_uniqueness_check_constraints_in_address(self):
        """Check keys in the Person.Address table"""
        expected_res = [['FK_Address_StateProvince_StateProvinceID'],
                        ['PK_Address_AddressID']]  # list of keys in the table
        df = self.get_dataframe("""
                                    Select CONSTRAINT_NAME
                                           ,TABLE_NAME
                                    From INFORMATION_SCHEMA.TABLE_CONSTRAINTS;
                                """)
        actual_df = df[['CONSTRAINT_NAME']][(df['TABLE_NAME'] == 'Address')]
        actual_df = actual_df.values.tolist()
        assert actual_df == expected_res, \
            "Check the availability of keys in the table"

    def test_validity_check_min_max_values_in_document(self):
        """ Check min and max values of the 'Revision' field
            in the Production.Document table"""
        expected_res = {'Revision': {'min': '0    ', 'max': '8    '}}
        df = self.get_dataframe("""
                                    Select *
                                    From [Production].[Document];
                                """)
        actual_df = df[['Revision']].agg(['min', 'max']).to_dict()
        assert actual_df == expected_res, \
            "Min and max values of the 'Revision' field are incorrect"

    def test_timelines_in_address(self):
        """ Check the ModifiedDate field in the Person.Address table"""
        expected_res = 0  # no updates after 2020
        df = self.get_dataframe("""
                                    Select *
                                    From [Person].[Address];
                                """)
        actual_df = df[(df['ModifiedDate'] > '2020-01-01')].shape[0]
        assert actual_df == expected_res, "There should be no such rows."

    def close(self):
        pass
