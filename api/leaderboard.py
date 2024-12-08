from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from model.vote import Vote
from model.post import Post
from model.user import User

leaderboard_api = Blueprint('leaderboard_api', __name__, url_prefix='/api')
api = Api(leaderboard_api)

class LeaderboardAPI:
    class _Leaderboard(Resource):
        def get(self):
            posts = Post.query.all()
            post_vote_counts = []

            for post in posts:
                user = User.query.filter_by(id=post.user_id).first()
                votes = Vote.query.filter_by(_post_id=post.id).all()
                upvotes = len([vote for vote in votes if vote._vote_type == 'upvote'])
                downvotes = len([vote for vote in votes if vote._vote_type == 'downvote'])
                net_vote_count = upvotes - downvotes

                post_vote_counts.append({
                    'post_id': post.id,
                    'post_title': post.title,
                    'user_id': user.id,
                    'username': user.username,
                    'upvotes': upvotes,
                    'downvotes': downvotes,
                    'net_vote_count': net_vote_count
                })

            return jsonify(post_vote_counts)

api.add_resource(LeaderboardAPI._Leaderboard, '/leaderboard')