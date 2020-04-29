exports.handler = function(event, context) {

var request = require('request');
var cheerio = require('cheerio');

var myKEY = '';
var myVAL = '';

const RESULTS_ALL = {};
const RESULTS_UP = {};
const RESULTS_DOWN = {};
const RESULTS_MAINT = {};

var COUNT_UP = 0;
var COUNT_DOWN = 0;
var COUNT_INFO = 0;
var COUNT_REVIEW = 0;

const OBJECT = { 'Ally':'ally',
                 'Analytics - Managed Hosting':'analytics---managed-hosting',
                 'Behind The Blackboard':'behind-the-blackboard',
                 'Collaborate - I.M.':'blackboard-collaborate---blackboard-im',
                 'Collaborate - Web Conferencing Canada':'blackboard-collaborate---web-conferencing-canada-hosted',
                 'Collaborate - U.S.':'blackboard-collaborate---web-conferencing-us-hosted',
                 'Developer Portal':'developer-portal---developer-blackboard-com',
                 'Learn - Blackboard Open Content':'xplor',
                 'Learn - Cloud & Social Tools':'cloud--social-tools',
                 'Learn - Inline Grading - New Box View':'inline-grading-crocodoc',
                 'Learn - Managed Hosting Canada':'learn---managed-hosting-canada',
                 'Learn - Managed Hosting U.S.':'blackboard-learn-data-centers',
                 'Learn - Mobile Services':'learn---mobile-services',
                 'Learn - Partner Clooud':'partner-cloud',
                 'Learn - SaaS Deployment U.S.':'saas-deployment-for-blackboard-learn',
                 'Moodlerooms U.S.':'moodlerooms',
                 'Moodlerooms Enterprise':'enterprise-moodle',
                 'SafeAssign':'safeassign'
                };
                 

const RESULTS = {};

request('http://status.blackboard.com', function (error, response, html) {
    if (!error && response.statusCode == 200) {
        var $ = cheerio.load(html);

        for (const [key, value] of Object.entries(OBJECT)) {
            myVAL = '#' + OBJECT[key];
            var tempVAR = $(myVAL).find('img').attr('alt');
//            console.log(key, tempVAR);

            if (tempVAR == 'Up') {
                Object.assign(RESULTS_UP, {key: ' is UP.'});
                Object.assign(RESULTS_ALL, {key: ' is UP.'});
                COUNT_UP = COUNT_UP + 1;
                }
            else if (tempVAR == 'Down') {
                Object.assign(RESULTS_DOWN, {key: ' is down or substantially degraded.'});
                Object.assign(RESULTS_ALL, {key: ' is down or substantially degraded.'});
                COUNT_DOWN = COUNT_DOWN + 1;
                }
            else if (tempVAR == "Maintenance"){
                Object.assign(RESULTS_MAINT, {key: ' should be review for recent maintenance.'});
                Object.assign(RESULTS_ALL, {key: ' should be review for recent maintenance.'});
                COUNT_REVIEW = COUNT_REVIEW + 1;
                }
            }
         
        }
    });

    for (const key of Object.keys(RESULTS_UP)) {
        const value = RESULTS_UP[key];
        console.log(`${key} -> ${value}`);
    }
    
};
