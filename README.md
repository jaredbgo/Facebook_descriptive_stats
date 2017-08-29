# Facebook_descriptive_stats
Program delivering descriptive statistics about groups of Facebook posts

This program groups posts into paid posts (those with paid facebook boosting) and unpaid posts. Next, it prints descriptive statistics for the following groups: Posts of different lengths, bosts at lunch time (11:00 AM to 1:00 PM) vs. dinner time (7:00 PM to 10:00 PM), posts with a questions vs. those with no questions, posts with videos vs. posts with images. 

Step 1: Go to https://developers.facebook.com/tools/explorer/ and log in to your facebook account
- Click "Get Token" and be sure to check off "user_managed_groups"(if you want to analyze a group you manage), "user_posts" (if you want to analyze your own page), and "read_insights" (YOU MUST CHECK THIS OFF SO THE PROGRAM RETURNS ANALYTICAL INSIGHT DATA)
- Click "Get Access Token", copy the generated token, and assign it to the variable "access_token" as a string on line 83

Step 2: Go to https://findmyfbid.com/, copy the url of the facebook page you are hoping to analyze, copy and paste on line 85 to assign to the variable "facebook_user_id".

Descriptive statistics for each question, organized by paid and unpaid posts, will be posted in the output. 
