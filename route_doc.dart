const domain = '192.168.43.0';
const baseUrl = 'http://$domain';
const authPrefix = '/auth';
const categoryPrefix = '/categories';
const topicsPrefix = '/topics';
const quizPrefix = '/quiz';
const followPrefix = '/follow';

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
  user(authPrefix, '/user', requiresAuth: false),
  find(authPrefix, '/find', queryParams: ['email=kingcollins172@gmail.com']),
  //------------------------------
  profile(authPrefix, '/profile'),

  createProfile(
    authPrefix,
    '/profile/create',
    method: _Method.post,
    body: profileBody,
  ),
  updateProfile(
    authPrefix,
    '/profile/update',
    method: _Method.put,
    body: profileBody,
  ),
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
      queryParams: ['following=True', 'category=1']),
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
  quiz(quizPrefix, '', queryParams: ['topic=4'], body: pageInfoBody),
  quizFromCategory(
    quizPrefix,
    '/',
    body: pageInfoBody,
    queryParams: ['level=400'],
    extras:
        'This route takes in a path parameter of the category_id thus; /<category_id>',
  ),
  suggestedQuiz(
    quizPrefix,
    '/suggested',
    body: pageInfoBody,
    requiresAuth: true,
  ),
  //-------------------------------------

  follow(followPrefix, '',
      requiresAuth: true, queryParams: ['id=7'], method: _Method.post),
  unfollow(followPrefix, '',
      requiresAuth: true, queryParams: ['id=7'], method: _Method.delete),
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

void main() {
  print(APIUrl.quizFromCategory.doc);
}
