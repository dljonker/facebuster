import psycopg2

def save_account_code():
    global account_code
    account_code = input("Insira o código da conta: ")

    with open("AccountCode.txt", "w") as file:
        file.write(account_code)

def save_lines_with_foto(input_file, output_file):
    with open(input_file, 'r') as file:
        lines_with_foto = [line for line in file if 'foto' in line.lower()]

    with open(output_file, 'w') as file:
        file.writelines(lines_with_foto)

def extract_pin():
    pin_lines = []
    with open('output.txt', 'r') as file:
        for line in file:
            if 'foto da pessoa' in line:
                start_index = line.find('foto da pessoa') + len('foto da pessoa')
                end_index = line.find(',', start_index)
                pin = line[start_index:end_index].strip().replace(' ', '')
                pin_lines.append(pin + '\n')

    with open('pin.txt', 'w') as file:
        file.writelines(pin_lines)

def search_pins_in_database():

    with psycopg2.connect(
        host='localhost',
        port='7020',
        user='guest',
        password='guest',
        database='situator'
    ) as conn:
        with conn.cursor() as cursor:
            with open('pin.txt', 'r') as file:
                with open('ids.txt', 'w') as output_file:
                    for line in file:
                        pin = line.strip()
                        cursor.execute(
                            """SELECT * FROM "PersonPin" WHERE "Pin" = %s AND "AccountId" = %s""",
                            (pin, account_code)
                        )
                        result = cursor.fetchone()
                        if result:
                            output_file.write(f"{result}\n")

def search_names_in_database():
    with psycopg2.connect(
        host='localhost',
        port='7020',
        user='guest',
        password='guest',
        database='situator'
    ) as conn:
        with conn.cursor() as cursor:
            with open('ids.txt', 'r') as file:
                with open('names.txt', 'w') as output_file:
                    for line in file:
                        result_id = line.strip().split(',')[0].replace('(', '')
                        cursor.execute(
                            """SELECT "Name" FROM "Person" WHERE "Id" = %s""",
                            (result_id,)
                        )
                        result = cursor.fetchone()
                        if result:
                            output_file.write(f"{result[0]}\n")

# Criado por Davy L. Jonker
input_file = 'C:\ProgramData\Seventh\Situator\Logs\Situator.log'
output_file = 'output.txt'

print(f'O "Busca Fotos" lê o arquivo de log mais atual e procura por informações de fotos que falharam ao ser enviadas ao dispositivo\npermitindo que os cadastros com problema possam ser rapidamente localizados')

save_account_code()

print(f'A conta com código {account_code} foi salva no arquivo AccountCode.txt...')

save_lines_with_foto(input_file, output_file)

print(f'\nArquivo Situator.log verificado... ')

extract_pin()

print(f'Extraindo informações de pin...')

print(f'Executando consultas no banco...')

search_pins_in_database()

search_names_in_database()

print(f'\nNomes dos cadastros com problemas salvos no arquivo names.txt')

# Closing the database connection

#conn.close()

# End message
input("Aperte qualquer tecla para finalizar...")