const axios = require('axios');

exports.handler = async (event, context) => {

  const STEPZEN_API_KEY = process.env.STEPZEN_API_KEY;

  let sub_id = event.queryStringParameters.sub_id;

  const data = {
    query: `
      query getArticleDetailsByID($collection: String, $dataSource: String, $database: String, $filter: JSON)
      {
        getArticleDetailsByID(
          collection: $collection,
          dataSource: $dataSource,
          database: $database,
          filter: $filter)
        {
          document {
            title
            score
            submission_id
            author_fullname
            subreddit_name_prefixed
            comments {
              comment_id
              body
              body_html
              score
              author_fullname
              replies {
                reply_id
                author_fullname
                body
                body_html
              }
            }
          }
        }
      }
    `,
    variables: {
      collection: "articles",
      database: "reddit",
      dataSource: "Cluster0",
      filter: {submission_id: sub_id}
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