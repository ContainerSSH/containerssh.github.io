<h1>Roadmap</h1>

<div id="roadmap"><p>Please wait...</p></div>
<script type="module">
import { Octokit } from "https://cdn.skypack.dev/@octokit/core";
const roadmap = async function(root) {
    try { 
        const octokit = new Octokit();
        const issues = await octokit.request("GET /repos/{owner}/{repo}/issues", {
            owner: "ContainerSSH",
            repo: "ContainerSSH"
        });
        const response = await octokit.request("GET /repos/{owner}/{repo}/milestones", {
            owner: "ContainerSSH",
            repo: "ContainerSSH"
        });
        root.innerHTML = "";
        for (const milestone of response.data) {
            const heading = document.createElement("h2");
            const headingLink = document.createElement("a");
            headingLink.href = milestone.html_url;
            headingLink.target = "_blank";
            headingLink.rel="noreferer noopener";
            headingLink.innerText = milestone.title;
            heading.appendChild(headingLink);
            root.appendChild(heading);
            const rendered = await octokit.request("POST /markdown", {
                text: milestone.description
            });
            const description = document.createElement("p");
            description.innerHTML = rendered.data;
            root.appendChild(description);
            const ul = document.createElement("ul");
            ul.className = "task-list";
            root.appendChild(ul); 
            for (const issue of issues.data) {
                if (issue.milestone !== null && milestone.id === issue.milestone.id) {
                    const li = document.createElement("li");
                    li.className = "task-list-item";
                    const label = document.createElement("label");
                    label.className = "task-list-control";
                    const input = document.createElement("input");
                    input.type = "checkbox";
                    input.disabled = true;
                    if (issue.closed_at !== null) {
                        input.checked = true
                    }
                    label.appendChild(input);
                    const span = document.createElement("span");
                    span.className = "task-list-indicator";
                    label.append(span);
                    li.appendChild(label);
                    const issueLink = document.createElement("a");
                    issueLink.href = issue.html_url;
                    issueLink.target = "_blank";
                    issueLink.rel="noreferer noopener";
                    const text = document.createTextNode("#" + issue.number + ": " + issue.title);
                    issueLink.appendChild(text);
                    li.appendChild(issueLink);
                    const issueBody = document.createElement("p");
                    const issueBodyRendered = await octokit.request("POST /markdown", {
                        text: issue.body
                    });
                    issueBody.innerHTML = issueBodyRendered.data;
                    li.appendChild(issueBody);
                    ul.appendChild(li)
                }
            }
        }
    } catch {
        root.innerHTML = "We are currently unable to fetch the roadmap. Please <a href=\"https://github.com/ContainerSSH/ContainerSSH/milestones\" target=\"_blank\" rel=\"noreferer noopener\">take a look on GitHub</a>.";
    }    
};
roadmap(document.getElementById("roadmap"));
</script>