from flask import Flask
from flask_restful import Resource, Api, reqparse

import scraper, json

app = Flask(__name__)
api = Api(app)


class MPList(Resource):
    def get(self):
        list = scraper.mps_json

        return {"data": list}, 200


class MPVotes(Resource):
    def get(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument("personId", required=True)
        args = parser.parse_args()

        votes = scraper.scrape_mp_votes(args["personId"])
        votes_json_string = json.dumps(votes, ensure_ascii=False, indent=4)

        mp = next(
            match for match in scraper.mp_list if match["person_id"] == args["personId"]
        )

        return {f"{mp['name']}_voting_data": votes}, 200


class MPName(Resource):
    def get(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument("personId", required=True)
        args = parser.parse_args()

        # mp_name = pass

        mp = next(
            match for match in scraper.mp_list if match["person_id"] == args["personId"]
        )

        return {"name": mp["name"]}, 200


class MPData(Resource):
    def get(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument("personId", required=True)
        args = parser.parse_args()

        # mp_name = pass

        mp = next(
            match for match in scraper.mp_list if match["person_id"] == args["personId"]
        )

        return {"mp_data": mp}, 200


api.add_resource(MPList, "/get_mp_list")
api.add_resource(MPVotes, "/get_mp_votes")
api.add_resource(MPName, "/get_mp_name")
api.add_resource(MPData, "/get_mp_data")


@app.route("/")
def index():
    return "<h1> Deployed to Heroku</h1>"


if __name__ == "__main__":
    app.run()  # run our Flask app
