import argparse

#tworzymy obiekt parsera
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")

...
#Czasem potrzebujemy dodać parametr, który funkcjonuje na zasadzie flagi.
# Interesuje nas tylko, czy jest ustawiony, czy nie.
parser.add_argument("-l", "--list", help="list users", action="store_true")

...
#Jak już zadeklarujemy wymagane przez nas argumenty, musimy wywołać metodę z naszego parsera, która je sparsuje
args = parser.parse_args()
#Od teraz, wszystkie argumenty mamy dostępne w obiekcie args, jako atrybuty tego obiektu. Odwołujemy się do nich
# po kropce, korzystając z pełnej nazwy.
...
print(args.username)

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
args = parser.parse_args()
print(args.username)

#in the console
python3 users.py -u brajanusz
brajanusz