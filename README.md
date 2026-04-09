# oschvr.com

Personal blog about software, cloud, security, money, business, travelling and life.

Built with [Hugo](https://gohugo.io/) and the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme.

## Usage

### Run locally

```sh
hugo server -D
```

### Create a new post

```sh
hugo new content/posts/$(date "+%Y/%m/%d")/test.md
```

### Editor

Local post editor with S3 image upload (requires AWS CLI configured):

```sh
python3 editor/server.py
```

Opens at [http://localhost:8080](http://localhost:8080).

### Build

```sh
hugo
```
