from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import search
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('query')
indexdir = "indexdir"
ix = search.Load(indexdir)


class ChatBot(Resource):
    def post(self):
        args = parser.parse_args()
        print(args)
        query = args['query']
        result = search.Search(query, ix)
        return result


api.add_resource(ChatBot, '/chatbot')

if __name__ == '__main__':
    app.run(debug=False)
