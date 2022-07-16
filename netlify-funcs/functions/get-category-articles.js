const axios = require('axios');

exports.handler = async (event, context) => {

  const STEPZEN_API_KEY = process.env.STEPZEN_API_KEY;

  let category = event.queryStringParameters.category;

  const data = {
    query: `
      query getArticlesByCategory($collection: String, $dataSource: String, $database: String, $filter: JSON, $sort: JSON, $limit: Int)
      {
        getArticlesByCategory(
          collection: $collection,
          dataSource: $dataSource,
          database: $database,
          filter: $filter,
          sort: $sort,
          limit: $limit)
        {
          documents {
            title
            score
            submission_id
            author_fullname
            subreddit_name_prefixed
          }
        }
      }
    `,
    variables: {
      collection: "articles",
      database: "reddit",
      dataSource: "Cluster0",
      filter: {"subreddit": category},
      sort: {"score": -1},
      limit: 25
    },
  };

  const payload = JSON.stringify(data);

  const headers = {
    'Accept': "application/json",
    'Content-Type': "application/json",
    'Authorization': STEPZEN_API_KEY
  }


  let response;
  try {
    response = await axios.post("https://konjic.stepzen.net/api/reddit-insights/__graphql", payload, {
      headers: headers});

    } catch (err) {
      return {
        statusCode: err.statusCode || 500,
        body: JSON.stringify({
          error: err.message
        })
      }
    }

  return {
    statusCode: 200,
    body: JSON.stringify(response.data),
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Allow-Methods": "GET, POST",
    },
  }
}