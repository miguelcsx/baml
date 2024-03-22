<a href="https://boundaryml.com?utm_source=github" target="_blank" rel="noopener noreferrer">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://www.boundaryml.com/gloo-ai-square-256.png">
    <img src="https://www.boundaryml.com/gloo-ai-square-256.png" height="64">
  </picture>
</a>

## BAML: A programming language to get structured data from LLMs</h2>

<div>
<a href="https://discord.gg/ENtBB6kkXH"><img src="https://img.shields.io/discord/1119368998161752075.svg?logo=discord&label=Discord%20Community" /></a>
<a href="https://twitter.com/intent/follow?screen_name=boundaryml"><img src="https://img.shields.io/twitter/follow/boundaryml?style=social"></a>

<a href="https://docs.boundaryml.com"><img src="https://img.shields.io/badge/Docs-Language_Tour-blue?logo=readthedocs" /></a>
<a href="https://docs.boundaryml.com"><img src="https://img.shields.io/badge/Docs-Syntax_Reference-blue?logo=readthedocs" /></a>
<a href="https://docs.boundaryml.com"><img src="https://img.shields.io/badge/Docs-Prompt_Engineering_Tips-blue?logo=readthedocs" /></a>

Supporting Tools

<a href="https://docs.boundaryml.com/v3/home/installation"><img src="https://img.shields.io/badge/BAML_Compiler-0.14.0-purple?logo=rust" /></a>
<a href="https://marketplace.visualstudio.com/items?itemName=gloo.baml"><img src="https://img.shields.io/badge/BAML_Extension-Testing_&_Live_Prompt_Preview-purple?logo=visualstudiocode" /></a>
<a href="https://app.boundaryml.com"><img src="https://img.shields.io/badge/Boundary_Studio-Observability_for_BAML-purple" /></a>

<hr />
</div>

<p>

Calling LLMs in your code is frustrating:

- your code uses types everywhere: classes, enums, and arrays
- but LLMs speak English, not types.

BAML makes calling LLMs easy by taking a schema-first approach:

- define schemas for your inputs and outputs,
- define prompt templates using these schemas, and
- compile your schemas and templates into a Python/TS client.

We've seen this pattern before plenty of times: [protobuf] and [OpenAPI] for RPCs, [Prisma] and [SQLAlchemy] for databases. BAML brings this pattern to LLMs.

[Show me some BAML code](#show-me-the-code)!

[protobuf]: https://protobuf.dev
[OpenAPI]: https://github.com/OpenAPITools/openapi-generator
[Prisma]: https://www.prisma.io/
[SQLAlchemy]: https://www.sqlalchemy.org/

We can generate clients in
<img src="https://img.shields.io/badge/Python-3.8+-default?logo=python" />
<img src="https://img.shields.io/badge/Typescript-Node_18+-default?logo=typescript" />

and have built a wide array of tools to give you a great developer experience:

| BAML Tooling                            | Capabilities                                                                                                              |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| BAML Compiler                           | Transpiles BAML code to a native Python / Typescript library <br />(you only need it for development, never for releases) |
| VSCode Extension                        | Syntax highlighting for BAML files<br /> Real-time prompt preview <br /> Testing UI                                       |
| Boundary Studio <br />(not open source) | Type-safe observability <br />Labeling                                                                                    |

</p>

<table>

<tr>
<td width="50%" style="vertical-align: top">

## Use cases

✅ Function calling ([code](#function-calling))<br />_Using tools_

✅ Classification ([code](#classification))<br />_Getting intent from a customer message_

✅ Extraction ([code](#show-me-the-code))<br />_Extracting a Resume data model from unstructed text_

✅ Agents <br />
_Orchestrating multiple prompts to achieve a goal_

🚧 Images<br />
_Coming soon_

</td>
<td width="50%" style="vertical-align: top">

## Prompt Examples

✅ Chain of thought ([code](#chain-of-thought))<br />
_Using techniques like reasoning_

✅ Multi-shot ([code](#multi-shot))<br/>
_Adding examples to the prompt_

✅ Symbol tuning ([code](#symbol-tuning))<br/>
_Using symbolic names for data-types_

✅ Multiple chat roles ([code](#comparing-multiple-prompts--llms))<br />
_Use system / assistant / whatever you want. We standardize it for all models_

</td>
</tr>
</table>

## Developer experience

✅ Type-safe guarantee<br />
_The LLM will return your data model, or we'll raise an exception_

✅ Fast iteration loops ([code](#comparing-multiple-prompts--llms))<br />
_Compare multiple prompts / LLM providers in VSCode_

🚧 Streaming partial jsons ([code](#streaming))<br />
✅ Python
🚧 Typescript<br />
_BAML parses incomplete jsons as it come in_

✅ LLM Robustness for production ([code](#robust-llm-calls))<br />
_Retry policies, Fallback strategies, Round-robin selection_

✅ Many LLM providers<br />
_OpenAI, Azure, Anthropic out-of-the-box. Reach out to get beta access for Mistral and more_

## Show me the code...

> For now this readme use rust syntax highlighting, but once we have 200 repos using BAML, [Github will support BAML](https://github.com/github-linguist/linguist/blob/master/CONTRIBUTING.md#adding-a-language)!

```rust
// extract_resume.baml

// 1. Defining the data model.
class Resume {
  name string
  education Education[]
}

class Education {
  university string
  start_year int
  end_year int? @description("unset if still in school")
}

// 2. Define the function signature
function ExtractResume {
  input (resume_text: string)
  output Resume
}

// 3. Write an implementation of ExtractResume
impl<llm, ExtractResume> version1 {
  client GPT4Client
  // BAML will automatically dedent and strip the
  // prompt for you.
  prompt #"
    Extract the resume from:
    ###
    {#input.resume_text}
    ###

    Output JSON Schema:
    {//
      This is macro for injecting your data model
      And yes, this is a comment in the prompt.
      Scroll down to see what it looks like with
      BAML syntax highlighting.
    //}
    {#print_type(output)}
  "#
}

// You can define clients either in the same file or different files.
client<llm> GPT4Client {
  provider "baml-openai-chat"
  options {
    model "gpt-4"
    api_key env.OPENAI_API_KEY
    // temperature 0.5 // Is 0 by default
  }
}
```

### See the prompt and test it in VSCode

<img src="docs/images/v3/prompt_view.gif" />

<img src="docs/images/v3/test-extract.gif" />

### Use your BAML function in your Python/Typescript app

#### Python

```python
# baml_client is auto
from baml_client import baml as b
# BAML also auto generates types for all your data models.
from baml_client.baml_types import Resume
import typing

async def get_resume(file_names: typing.List[str]) -> typing.List[Resume]:
  resumes = []
  for name in file_names:
    with open(name, 'r') as file:
      content = file.read()
      # Call your baml function
      # (This is a type-safe function w/ autocomplete!)
      resume = await b.ExtractResume(resume_text=content)
      assert isinstance(resume, Resume) # Not required, BAML already guarantees this!
      resumes.append(resume)
  return resumes
```

#### Typescript

```typescript
// The baml_client library is auto generated with the `baml build` command.
// Its usable w/o any dependency on baml.
import baml as b from "@/baml_client";
import { Resume } from "@/baml_client/types";
import fs from "fs";

function getResume(fileNames: string[]): Promise<Resume[]> {
  // Using map to transform fileNames into an array of Promises of Resume
  const resumePromises: Promise<Resume>[] = fileNames.map((name) => {
    // Read file content synchronously
    const content = fs.readFileSync(name, { encoding: "utf-8" });
    // Call your BAML function
    // BAML guarantees this function will return a resume type.
    // Type-safe w/ autocomplete
    return b.ExtractResume({ resumeText: content });
  });

  // Using Promise.all to wait for all promises to resolve
  return Promise.all(resumePromises);
}
```

## Comparing multiple prompts / llms

In BAML you do this by declaring multiple `impls`.

```rust
// Same signature as above
function ExtractResume {
  input (resume_text: string)
  output Resume
  // Declare which impl is the default one my python/ts code calls
  default_impl version1
}

// My original impl
impl<llm, ExtractResume> version1 {
  client GPT4Client
  prompt #"
    Extract the resume from:
    ###
    {#input.resume_text}
    ###

    Output JSON Schema:
    {#print_type(output)}
  "#
}

// My new and super improved impl
impl<llm, ExtractResume> with_chat_roles {
  // Since resumes are faily easy, i'll try claude here
  client ClaudeClient
  prompt #"
    {#chat(system)}
    You are an expert tech recruiter.
    Extract the resume from TEXT.

    {#chat(user)}
    TEXT
    ###
    {#input.resume_text}
    ###

    {#chat(assistant)}
    Output JSON Schema:
    {#print_type(output)}
  "#
}

// another client definition
client<llm> ClaudeClient {
  provider "baml-anthropic-chat"
  options {
    model "claude-3-haiku-20240307"
    api_key env.ANTHROPIC_API_KEY
  }
}
```

### Test them both

<img src="docs/images/v3/testing_2.gif" />

## Classification

```rust
// This will be available as an enum in your Python and Typescript code.
enum Category {
    Refund
    CancelOrder
    TechnicalSupport
    AccountIssue
    Question
}

function ClassifyMessage {
  input string
  output Category
}

impl<llm, ClassifyMessage> version1 {
  client GPT4
  prompt #"
    Classify the following INPUT into ONE
    of the following Intents:

    {// print_enum is a macro provided by BAML //}
    {#print_enum(Category)}

    INPUT: {#input}

    Response:
  "#
}
```

## Function Calling

```rust
class GithubCreateReleaseParams {
  owner string
  repo string
  tag_name string
  target_commitish string
  name string
  body string
  draft bool
  prerelease bool
}

function BuildGithubCreateReleaseParams {
  input string
  output GithubCreateReleaseParams
}

impl<llm, BuildGithubCreateReleaseParams> v1 {
  client GPT35
  prompt #"
    Given the following release instructions, craft a JSON payload matching
    the schema that describes the release that should be created:

    Instructions
    {#input}

    Schema:
    {#print_type(output)}

    JSON:
  "#
}
```

## Agents

Examples coming soon! Reach out <a href="https://discord.gg/ENtBB6kkXH">Boundary's Discord</a> if you want to do this before we publish them.

## Robust LLM calls

We make it easy to add [retry policies] to your LLM calls (and also provide other [resilience strategies]):

[retry policies]: https://docs.boundaryml.com/v3/syntax/client/retry
[resilience strategies]: https://docs.boundaryml.com/v3/syntax/client/client#fallback

```rust
client<llm> GPT4Client {
  provider "baml-openai-chat"
  retry_policy SimpleRetryPolicy
  options {
    model "gpt-4"
    api_key env.OPENAI_API_KEY
  }
}

retry_policy SimpleRetryPolicy {
    max_retries 5
    strategy {
      type exponential_backoff
      delay_ms 300
      multiplier 1.5
    }
}
```

## Chain-of-thought

To do planning with BAML, just tell the LLM what planning steps to do. BAML will automatically find your data objects and convert them automatically.

```rust
impl<llm, GetOrderInfo> version1 {
  client GPT4
  prompt #"
    Given the email below:

    Email Subject: {#input.subject}
    Email Body: {#input.body}

    Extract this info from the email in JSON format:
    {#print_type(output)}

    Schema definitions:
    {#print_enum(OrderStatus)}

    Before you output the JSON, please explain your
    reasoning step-by-step. Here is an example on how to do this:
    'If we think step by step we can see that ...
     therefore the output JSON is:
    {
      ... the json schema ...
    }'
  "#
}
```

## Multi-shot

To add examples into your prompt with BAML, you can use a second parameter:

```rust
function DoSomething {
  input (my_data: int, examples: string)
  output string
}

impl<llm, DoSomething> v1 {
  client GPT4
  prompt #"
    Given DATA do something cool!

    DATA: {#input.my_data}

    Examples:
    {#input.examples}
  "#
}
```

## Symbol-tuning

Sometimes using abstract names as "symbols" (e.g. k1, k2, k3…) allows the LLM to focus on your rules better.

- [research paper](https://arxiv.org/abs/2305.08298)
- Also used by OpenAI for their [content moderation](https://openai.com/blog/using-gpt-4-for-content-moderation).

```rust
// Enums will still be available as Category.Refund
// BAML will auto convert k1 --> Category.Refund for you :)
enum Category {
    Refund @alias("k1")
    @description("Customer wants to refund a product")

    CancelOrder @alias("k2")
    @description("Customer wants to cancel an order")

    TechnicalSupport @alias("k3")
    @description("Customer needs help with a technical issue unrelated to account creation or login")

    AccountIssue @alias("k4")
    @description("Specifically relates to account-login or account-creation")

    Question @alias("k5")
    @description("Customer has a question")

    // Skip this category for the LLM
    Bug @skip
}

// whenever you now use:
// {#print_enum(Category)}
// BAML will substitute in the alias and description automatically
// and parse anything the LLM returns into the appropriate type
```

## Streaming

BAML is able to offer streaming for partial jsons out of the box. No changes to BAML files, just call a different python function (TS support coming soon).

```python
async def main():
    async with b.ExtractResume.stream(resume_text="...") as stream:
        async for output in stream.parsed_stream:
            if output.is_parseable:
              # name is typed with None | str (in case we haven't gotten the name field in the response yet.)
              name = output.parsed.name
              print(f"streaming: {output.parsed.model_dump_json()}")

            # You can also get the current delta. This will always be present.
            print(f"streaming: {output.delta}")

        # Resume type
        final_output = await stream.get_final_response()
        if final_output.has_value:
            print(f"final response: {final_output.value}")
        else:
            # A parsing error likely occurred.
            print(f"final resopnse didnt have a value")
```

## Observability

Analyze, label, and trace each request in Boundary Studio.

<img src="docs/images/v3/pipeline_view.png" width="80%" alt="Boundary Studio">

### [Documentation](https://docs.boundaryml.com)

See more at [our docs page](https://docs.boundaryml.com)

### Resources

- [Discord](https://discord.gg/ENtBB6kkXH)

## Security

Please do not file GitHub issues or post on our public forum for security vulnerabilities, as they are public!

Boundary takes security issues very seriously. If you have any concerns about BAML or believe you have uncovered a vulnerability, please get in touch via the e-mail address contact@boundaryml.com. In the message, try to provide a description of the issue and ideally a way of reproducing it. The security team will get back to you as soon as possible.

Note that this security address should be used only for undisclosed vulnerabilities. Please report any security problems to us before disclosing it publicly.

<hr />

Made with ❤️ by Boundary
