const domain = '192.168.43.0';
const baseUrl = 'http://$domain';
const authPrefix = '/auth';
const categoryPrefix = '/categories';
const topicsPrefix = '/topics';
const quizPrefix = '/quiz';
const followPrefix = '/follow';
const challengePrefix = '/challenge';
const questionsPrefix = '/questions';
const activityPrefix = '/activity';

///Holds all the details of the backend endpoints for the qeasily application
///Each enumeration is an endpoint in the app
enum APIUrl {
  //All "/auth" prefixed routes are here
  login(
    authPrefix,
    '/login',
    method: _Method.post,
    requiresAuth: false,
    body: {'email': 'jon@doe.com', 'password': 'password'},
  ),

  register(
    authPrefix,
    '/register',
    method: _Method.post,
    requiresAuth: false,
    body: {
      'user_name': 'Jon Doe',
      'email': 'jon@doe.com',
      'password': 'password'
    },
  ),
  search('/search', '',
      requiresAuth: false,
      body: pageInfoBody,
      queryParams: ['query=Test'],
      extras:
          'Searches the topics, quizzes and challenges database for the query'),
  user(authPrefix, '/user', requiresAuth: false),
  fetchDashboard(authPrefix, '/dashboard',
      method: _Method.get, requiresAuth: true),

  //
  createActivity(activityPrefix, '/create',
      method: _Method.post, requiresAuth: true),
  fetchActivity(activityPrefix, '', method: _Method.get, requiresAuth: true),
  consumerQuiz(activityPrefix, '/consume-quiz'),
  consumerChallenge(activityPrefix, '/consume-challenge', method: _Method.get),
  //------------------------------
  //------------------------------
  //All "/categories" prefixed route
  //--------------------------------
  categories(categoryPrefix, '/', requiresAuth: false),
  createCategories(
    categoryPrefix,
    '/create',
    method: _Method.post,
    body: [
      {'name': '', 'user_id': ''},
    ],
  ),
  updateCategory(
    categoryPrefix,
    '/update',
    method: _Method.put,
    body: {'id': '', 'name': '', 'user_id': ''},
  ),

  deleteCategory(
    categoryPrefix,
    '/delete',
    method: _Method.delete,
    queryParams: ['id=11'],
  ),

  //-------------------------------------
  //All "/topics" prefixed routes
  topics(topicsPrefix, '',
      requiresAuth: true,
      body: pageInfoBody,
      queryParams: ['following=true', 'category=1'],
      extras: 'The query parameters are exclusive'),
  createTopic(topicsPrefix, '/create', method: _Method.post, body: [
    {
      'title': '',
      'description': '',
      'date_added': '',
      'category_id': '',
      'user_id': ''
    }
  ]),
  deleteTopic(
    topicsPrefix,
    '/remove',
    requiresAuth: true,
    queryParams: ['topic=4'],
  ),
  //-------------------------------------
  //-------------------------------------
  //All "/quiz" prefixed routes
  fetchQuiz(quizPrefix, '', queryParams: ['topic=4'], body: pageInfoBody),
  quizFromCategory(
    quizPrefix,
    '/by-category',
    body: pageInfoBody,
    queryParams: ['cid=10&level=400'],
    extras:
        'This route takes in a path parameter of the category_id thus; /<category_id>',
  ),
  suggestedQuiz(
    quizPrefix,
    '/suggested',
    body: pageInfoBody,
    requiresAuth: true,
  ),
  createQuiz(quizPrefix, '/create', method: _Method.post, body: {
    'title': 'Test Quiz',
    'questions': [1, 4, 5, 66, 3, 2],
    'topic_id': 6,
    'duration': 2000,
    'description': 'A tough one',
    'difficulty': 'Medium',
    'type': 'mcq'
  }),
  fetchCreatedQuiz(quizPrefix, '/created-quiz', body: pageInfoBody),
  deleteQuiz(quizPrefix, '/delete',
      method: _Method.delete, queryParams: ['qid=19']),
  //-------------------------------------

  follow(followPrefix, '',
      requiresAuth: true, queryParams: ['id=7'], method: _Method.post),
  unfollow(followPrefix, '',
      requiresAuth: true, queryParams: ['id=7'], method: _Method.delete),
fetchAccountToFollow(followPrefix, '/accounts',
      method: _Method.get, requiresAuth: true, body: pageInfoBody),

  fetchFollowers(followPrefix, '/followers',
      body: pageInfoBody, method: _Method.get),

  fetchChallenges(challengePrefix, '',
      method: _Method.get, queryParams: ['feed=true'], body: pageInfoBody),


  fetchUserCreatedChallenges(challengePrefix, '/created-challenges',
      body: pageInfoBody),

  fetchChallengeDetails(
    challengePrefix,
    '/details',
    method: _Method.get,
    queryParams: ['cid=10'],
    extras: 'cid is Challenge Id',
  ),
  startChallenge(
    challengePrefix,
    '/start',
    method: _Method.get,
    queryParams: ['cid=6'],
    extras: 'Query this endpoint to enter a challenge. '
        'This endpoints initializes your entry in the leaderboards table',
  ),
  saveChallengeProgress(challengePrefix, '/save-progress',
      queryParams: ['cid=6', 'points=50'], method: _Method.post),

  fetchCurrentChallenges(challengePrefix, '/me',
      method: _Method.get,
      extras:
          'Fetches the  current challenges that a user is participating in'),

  createChallenge(
    challengePrefix,
    '/create',
    method: _Method.post,
    body: challengeBody,
  ),
  deleteChallenge(challengePrefix, '/delete',
      method: _Method.delete, queryParams: ['cid=6']),
  fetchCreatedChallenges(
    challengePrefix,
    '/created-challenge',
    body: pageInfoBody,
  ),
  fetchNextTask(
    challengePrefix,
    '/next-task',
    queryParams: ['cid=5'],
    extras: 'Fetches the next task of a challenge giving the users progress',
  ),

  fetchLeaderboards(
    challengePrefix,
    '/leaderboards',
    queryParams: ['cid=6'],
    body: pageInfoBody,
    method: _Method.get,
    extras: 'Fetch the leaderboards of a current challenge',
  ),
  //---------------------------------------------------------------------
  fetchQuizQuestions(questionsPrefix, '',
      body: pageInfoBody, queryParams: ['quiz_id=5']),
  fetchAllMcq(questionsPrefix, '/all-mcq',
      body: pageInfoBody, queryParams: ['topic_Id=4']),
  fetchCreatedDcq(questionsPrefix, '/created-dcq',
      body: pageInfoBody,
      queryParams: ['topic_id=5'],
      extras: 'topic_id can be none'),
  fetchAllDcq(questionsPrefix, '/all-dcq',
      body: pageInfoBody, queryParams: ['topic_id']),
  fetchCreatedMcq(questionsPrefix, '/created-mcq',
      body: pageInfoBody, queryParams: ['topic_id']),
  deleteMcq(questionsPrefix, '/delete',
      method: _Method.delete, body: [4, 6, 3, 1, 4]),
  deleteDcq(questionsPrefix, '/delete-dcq',
      method: _Method.delete, body: [6, 7, 4, 22, 5, 6]),
  createDcq(questionsPrefix, '/create-dcq',
      body: [
        {'query': '', 'correct': true, 'explanation': 'blah', 'topic_id': 5},
      ],
      method: _Method.post),
  createMcq(questionsPrefix, '/create-mcq',
      body: [
        {
          'query': '',
          'A': '',
          'B': '',
          'C': '',
          'D': '',
          'correct': 'A',
          'explanation': 'Blah',
          'topic_id': 5,
          'difficulty': 'Hard'
        }
      ],
      method: _Method.post),
  ;

  final String prefix, path;
  final String? extras;
  final bool requiresAuth;
  final List<String>? queryParams;
  final dynamic body;
  final _Method method;

  ///
  const APIUrl(
    this.prefix,
    this.path, {
    this.requiresAuth = true,
    this.queryParams,
    this.body,
    this.extras,
    this.method = _Method.get,
  });

  //whether the endpoint requires a body
  bool get requiresBody => body != null;

  String get url => (prefix + path);
  String get doc =>
      'APIUrlDoc{url: http://${domain}$url, method: $method, requiresAuthentication: $requiresAuth, '
      'params: $queryParams, body: $body}'
      '\n\n$extras';
}

enum _Method { get, post, put, delete }

const pageInfoBody = {'per_page': 10, 'page': 2};
const profileBody = {
  'first_name': '',
  'last_name': '',
  'reg_no': '',
  'department': '',
  'level': '',
  'user_id': ''
};

const challengeBody = {
  'name': 'Hot Challenge',
  'quizzes': [7, 6, 87, 3, 5],
  'paid': true,
  'entry_fee': 50.0,
  'reward': 5000,
  'duration': 7,
};

// void main() {
//   print(APIUrl.quizFromCategory.doc);
// }
