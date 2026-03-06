# BotArena Example Bots

Starter templates for [BotArena.Games](https://botarena.games) — copy, modify, and compete!

## Examples

| Bot | Language | Strategy | Game |
|-----|----------|----------|------|
| `random_connect4.py` | Python | Random valid move | Connect 4 |
| `random_connect4.js` | JavaScript | Random valid move | Connect 4 |
| `minimax_connect4.py` | Python | Minimax (depth 4) | Connect 4 |

## Getting Started

1. **Register your bot** at [botarena.games/register](https://botarena.games/register)
2. **Save your API key**
3. **Clone this repo** and pick an example
4. **Replace** `bot_your_api_key_here` with your key
5. **Run it** and watch it compete!

## API Quick Reference

```
WebSocket: wss://botarena.games/bot?apiKey=YOUR_KEY
Queue:     POST https://botarena.games/api/v1/real-matches/queue/join
           Header: x-api-key: YOUR_KEY
Docs:      https://botarena.games/docs
```

## Move Format (Connect 4)

```json
{ "column": 3 }
```

## Contributing

Submit your own example bot via Pull Request!
