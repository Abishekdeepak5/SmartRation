from app.supabase_config import supabase


def insertRow(tableName,dictData):
    return supabase.table(tableName).insert(dictData).execute()

def updateRow(tableName,dictData,columnName,id):
    return supabase.table(tableName).update(dictData).eq(columnName, id).execute()

def deleteRow(tableName,columnName,id):
    return supabase.table(tableName).delete().eq(columnName, id).execute()

def getRows(tableName):
    return supabase.table(tableName).select("*").execute()

def getRowsWithId(tableName,columnName,id):
    return supabase.table(tableName).select("*").eq(columnName,id).execute()


