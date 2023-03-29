 #importing pymongo to work with mongoDB
import pymongo

# connecting to local mongoDB server
server = pymongo.MongoClient("mongodb+srv://pmn23546:UBsIEiTaNS7QH3XL@cluster0.xpce3wc.mongodb.net/test")


if server:
    print(server)
else:
    print({'Error:' : 'connection to database failed' })
    exit(False)

# connecting to our database
db = server['sample']

# accessing out collection of 'dataset' where out sample data is collected
dataset = db['dataset']
print(dataset)

def authenticate_apikeys(apikey):
    # db = server['api_key']
    api_key = db['api_key']
    find = api_key.find_one({'apikey' : apikey})
    if find:
        return "valid"
    else:
        return "invalid"

# function to read data from mongodb database
def read_dataset(id):
    find = dataset.find_one({'id' : id})
    return find
# print(read_dataset(1003))
    
# function to write data to mongodb database
def write_dataset(first_name : str, last_name : str, email : str, gender : str, ip_address : str):
    id = dataset.count_documents({}) + 1
    dataset.insert_one({'id' : id, 'first_name' : first_name, 'last_name' : last_name, 'email' : email , 'gender' : gender, 'ip_address' : ip_address})

# write_dataset('pkp', 'praveen', 'pkp@gmail.com', 'male', '196.122.1.1')

