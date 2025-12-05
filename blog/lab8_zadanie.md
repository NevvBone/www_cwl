# Lab 8 - Zapytania GraphQL

## Zapytania (Queries)

### 1. Lista wszystkich postów z powiązaniami  
```graphql  
query {  
  allPosts {  
    id  
    title  
    text  
    slug  
    createdAt  
    createdBy {  
      id  
      username  
    }  
    topic {  
      id  
      name  
      category {  
        id  
        name  
      }  
    }  
  }  
}

```

### 2. Posty, których tytuł zawiera jakiś fragment  
```graphql  
query {  
  postsByTitleContains(substr: "www") {  
    id  
    title  
  }  
}

```

### 3. Posty danego użytkownika  
```graphql  
query {  
  postsByUsername(username: "NevvBone") {  
    id  
    title  
    createdAt  
  }  
}

```

### 4. Liczba postów danego użytkownika  
```graphql  
query {  
  postsCountByUserId(userId: 1)  
}

```

## Mutacje

### 1. Mutacja tworząca nowy post  
```graphql  
mutation {  
  createPost(  
    title: "Nowy post z GraphQL"  
    text: "Treść posta"  
    slug: "nowy-post-graphql"  
    topicId: 1  
    createdById: 1  
  ) {  
    post {  
      id  
      title  
      createdBy {  
        username  
      }  
    }  
  }  
}

```

### 2. Mutacja aktualizująca post  
```graphql  
mutation {  
  updatePost(  
    id: 1  
    title: "Zmieniony tytuł z GraphQL"  
  ) {  
    post {  
      id  
      title  
      updatedAt  
    }  
  }  
}

```

### 3. Mutacja usuwająca post  
```graphql  
mutation {  
  deletePost(id: 1) {  
    ok  
  }  
}

```

