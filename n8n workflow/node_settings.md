# this file explains the set up of each node in n8n workflow

# skeleton structure
gmail trigger->code in javascipt 1(build prompt node)->HTTP Request Node->Code in javascript->Firebase create node->Telegram node

# gmail trigger settings
connected to gmail account
poll time everyminute
event message recieved
filter read status unread emails only

# code in javascript 1
```
const data = $input.first().json;

const subject = data.Subject || data.subject || 
  data.headers?.Subject || data.headers?.subject || 'No Subject';

const fromRaw = data.From || data.from || 
  data.headers?.From || data.headers?.from || {};

let from = typeof fromRaw === 'string' 
  ? fromRaw 
  : fromRaw?.text || fromRaw?.value || 'Unknown';

// Remove double quotes that break JSON
from = from.replace(/"/g, '').replace(/'/g, '');

const snippet = (data.snippet || '').replace(/"/g, '').replace(/'/g, '');
const cleanSubject = subject.replace(/"/g, '').replace(/'/g, '');

const prompt = `You are a job application email classifier. Respond with ONLY valid JSON, no explanation, no markdown, no backticks. Email Subject: ${cleanSubject} Email From: ${from} Email Snippet: ${snippet} Rules: status must be exactly one of [Applied, OA, Technical, HR, Offer, Rejected]. company must be the EXACT company name from subject or sender, never invent one. role is the job role if mentioned else Software Engineer. message is one short friendly line. emoji is one relevant emoji. Respond ONLY with this JSON object with these exact keys: status, company, role, message, emoji`;

return [{
  json: {
    ...data,
    prompt: prompt,
    subjectClean: cleanSubject,
    fromClean: from
  }
}];
```

# HTTP Request node

method post
url https://api.groq.com/openai/v1/chat/completions
send header using field below
name authorisation
value Bearer GROK API KEY
name Content-Type
value application/json

send body =>on
body content specify content =>json 

```
{
  "model": "llama-3.1-8b-instant",
  "messages": [
    {
      "role": "user",
      "content": "={{ $json.prompt }}"
    }
  ]
}
```

# code in javascipt 
```
const data = $input.first().json;

// Grab subject and from from ALL possible locations
const subjectRaw = 
  data.Subject || 
  data.subject || 
  data.headers?.Subject || 
  data.headers?.subject ||
  data.payload?.headers?.find(h => h.name === 'Subject')?.value ||
  'Job Application';

const fromRaw = 
  data.From || 
  data.from || 
  data.headers?.From || 
  data.headers?.from ||
  data.payload?.headers?.find(h => h.name === 'From')?.value ||
  '';

// Parse Groq response
const groqText = data.choices?.[0]?.message?.content || '{}';

let classification;
try {
  const cleaned = groqText.replace(/```json|```/g, '').trim();
  classification = JSON.parse(cleaned);
} catch(e) {
  classification = {
    status: 'Applied',
    company: 'Unknown',
    role: 'Job Application',
    message: 'New email received',
    emoji: '📧'
  };
}

// Normalize status to exactly match dashboard values
const validStatuses = ['Applied', 'OA', 'Technical', 'HR', 'Offer', 'Rejected'];

let finalStatus = (classification.status || 'Applied').trim();
finalStatus = finalStatus.charAt(0).toUpperCase() + finalStatus.slice(1).toLowerCase();

const statusMap = {
  'Selected': 'Offer',
  'Hired': 'Offer',
  'Offered': 'Offer',
  'Hr': 'HR',
  'Technical round': 'Technical',
  'Online assessment': 'OA',
};

finalStatus = statusMap[finalStatus] || finalStatus;
if (!validStatuses.includes(finalStatus)) finalStatus = 'Applied';

// Clean up company name
let finalCompany = (classification.company || 'Unknown').trim();
finalCompany = finalCompany
  .replace(/['"]/g, '')
  .replace(/Inc\.?|LLC|Ltd\.?|Corp\.?/gi, '')
  .trim();
if (!finalCompany || finalCompany.length < 2 || finalCompany === 'Unknown') {
  // Last attempt — extract from subject directly
  const companyFromSubject = subjectRaw.match(/(?:at|in|from|by|with)\s+([A-Za-z]+)/i);
  finalCompany = companyFromSubject 
    ? companyFromSubject[1].charAt(0).toUpperCase() + companyFromSubject[1].slice(1)
    : 'Unknown';
}

// Clean up role
let finalRole = (classification.role || subjectRaw).trim();
if (finalRole.length > 60) finalRole = finalRole.substring(0, 60) + '...';

const today = new Date().toISOString().split('T')[0];

// Make document ID unique — emailId + timestamp
const uniqueId = (data.id || 'unknown') + '_' + Date.now();

return [{
  json: {
    email: 'shreyapant77@gmail.com',
    userId: 'Z8LSrfA6TDMcNoPcv7p1p5Oczx23',
    company: finalCompany,
    role: finalRole,
    status: finalStatus,
    dateApplied: today,
    timestamp: new Date().toISOString(),
    emoji: classification.emoji || '📧',
    message: classification.message || '',
    emailId: uniqueId,
    subject: subjectRaw,
    from: fromRaw
  }
}];
```

# firebase node set to create(earlier was set to update but it was overwriting the current entries so current settings changed to create)

```
Credential to connect with:Google Firebase Cloud Firestore account
Resource:Document
Operation:Create
Project Name or ID:applywise-web
Database:(default)
Collection:jobs
Document ID :empty
Columns / Attributes:email, company, role, status, dateApplied, timestamp, emoji, message, emailId
simplify on
 

```

# telegram node
```
Credential to connect with:Telegram account 2
Resource:Message
Operation:Send Message
Chat ID:YOUR TELEGRAM CHAT ID(this is accessed via telegram botfather then make you own bot then ask for id by first texing the bot hi to activate it)
text json type:
{{ $json.emoji }} *Job Application Update*

🏢 *Company:* {{ $json.company }}
🏷️ *Status:* {{ $json.status }}

{{ $json.message }}




Reply Markup
None
Additional Fields
Parse Mode
Markdown (Legacy)


```

//workflow complete (minor changes to be done)
