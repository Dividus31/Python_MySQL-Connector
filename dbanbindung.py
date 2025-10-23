from dataclasses import dataclass
from typing import Optional,List
import mysql.connector
from mysql.connector import Error,MySQLConnection

#Datenquelle aus Tabelle
@dataclass
class Adresse:
    id: Optional [int]
    name: str
    vorname: str
    strasse: str
    hausnummer: str
    plz: str
    stadt: str
    aenderungsdatum: str
    erfasst: str

#DB Verbindung mit return MySQL Connection Objekt
def get_connection(host:str="localhost",
    user:str="root",
    passwort:str="",
    database:str="adressenverwaltung") -> MySQLConnection:
    return mysql.connector.connect(host=host,
    user=user,
    password=passwort,
    database=database,
    auth_plugin="mysql_native_password")

#Repo Schicht

class AdressRepo:
    #Kapselung von Operationen fuer die Tabelle
    #Nur hier SQL Anweisungen
    def __init__(self,conn:MySQLConnection):
        self.conn=conn #Verbindung übergeben

    def create(self,adr:Adresse) -> int:
        sql = "INSERT INTO adressen (name,vorname,strasse,hausnummer,plz,stadt,geandertam,erfasstam) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        vals = (adr.name.strip(),adr.vorname.strip(),adr.strasse.strip(),adr.hausnummer.strip(),adr.plz.strip(),adr.stadt.strip(),adr.aenderungsdatum,adr.erfasst)
        with self.conn.cursor() as cur:
            cur.execute(sql,vals)
            self.conn.commit()
            return cur.lastrowid
    def get_by_id(self,id_:int) -> Optional[Adresse]:
        #Liest einen Datensatz aus aufgrund des PK Primary Key Primärschlüssel
        sql ="SELECT id, name, vorname, strasse, hausnummer, plz, stadt, geandertam, erfasstam FROM adressen WHERE id=%s"
        with self.conn.cursor(dictionary=True) as cur:
            cur.execute(sql, (id_,))
            row = cur.fetchone()
            if row is None:
                return None
            return Adresse(
                id=row["id"], 
                name=row["name"], 
                vorname=row["vorname"], 
                strasse=row["strasse"], 
                hausnummer=row["hausnummer"], 
                plz=row["plz"], 
                stadt=row["stadt"],
                aenderungsdatum=row["geandertam"],
                erfasst=row["erfasstam"]
            )
    def get_all(self) -> List[Adresse]:
        #Liest einen Datensatz aus aufgrund des PK Primary Key Primärschlüssel
        sql ="SELECT id,name,vorname,strasse,hausnummer,plz,stadt,geandertam,erfasstam FROM adressen"
        with self.conn.cursor(dictionary=True) as cur:
            cur.execute(sql)
            rows = cur.fetchall()

            return [Adresse(
                id=row["id"], 
                name=row["name"], 
                vorname=row["vorname"], 
                strasse=row["strasse"], 
                hausnummer=row["hausnummer"], 
                plz=row["plz"], 
                stadt=row["stadt"],
                aenderungsdatum=row["geandertam"],
                erfasst=row["erfasstam"]
            ) 
                for row in rows
            ]
    def search_by_name(self,suche:str) -> List[Adresse]:
        pass
    def update(self,adr:Adresse) -> bool:
        pass
    def delete(self,id:int) -> bool:
        pass

def main():
    try:
        #Verbindung aufbauen 
        conn=get_connection(host="localhost", user="root", passwort="", database="adressenverwaltung")
        if not conn.is_connected():
            print("Keine Verbindung möglich")

        repo = AdressRepo(conn)
        print("Daten anlegen:")
        aktion_id = repo.create(Adresse(None,"Müller","Michel", "Hauptstr.", "1", "55312", "Würzburg","2025-10-23", "2025-10-23"))
        print("Datensatz: ", aktion_id, " wurde angelegt")

        print("\nAlle Datensätze anzeigen:")
        adressen = repo.get_all()
        for adresse in adressen:
            print(f"ID: {adresse.id}, Name: {adresse.name}, Vorname: {adresse.vorname}, Adresse: {adresse.strasse} {adresse.hausnummer}, {adresse.plz} {adresse.stadt}")


    except Error as e:
        print(f"Error: {e}")
    
    finally:
        #Verbindung sauber schliessen
        try:
            conn.close()
        except Exception:
            pass
main()