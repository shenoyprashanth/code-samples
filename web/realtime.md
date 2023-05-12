## Long polling and SSE

```java

    private ExecutorService executor = Executors.newFixedThreadPool(5);
	
	/**
		The Thread.sleep() below in all the methods is supposed to mimic some computation.
		The time it takes to complete the computation in real world is dynamic.		
	**/


	/** 		
		In this version the client gets blocked for the duration of the computation ( 5 seconds in this example).
		If there was no data, then the client would again make a call to retrieve data.
	**/
    @GetMapping(value = "/blocking-call")
    public String blockingAPI() throws InterruptedException {
        Thread.sleep(5000);
        return "Hello";
    }

	/** 		
		In this version the client gets blocked for the duration of the computation ( 5 seconds in this example).
		However the server has setup a new thread to serve the request
	**/
    @GetMapping(value = "/long-polling")
    public DeferredResult<String> longPollingAPI() throws InterruptedException {
        DeferredResult<String> val = new DeferredResult<>();
        executor.execute(() -> {
            try {
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                val.setResult("Timed out");
            }
            val.setResult("Hello");
        });

        return val;
    }

	/** 
		In this version the client gets a hello every 5 seconds.
	**/
    @GetMapping("/sse")
    public Flux<ServerSentEvent<String>> sseAPI() {
        return Flux.interval(Duration.ofSeconds(5))
            .map(sequence -> ServerSentEvent.<String> builder()
                .data("Hello")
                .build());
    }
```

## WebSocket

```java

@Configuration
@EnableWebSocket
@Controller
public class WebSocketAPI implements WebSocketConfigurer {

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(socketHandler(),"/socket");;
    }

    @Bean
    public WebSocketHandler socketHandler() {
        return new SocketHandler();
    }

}

public class SocketHandler extends TextWebSocketHandler {

    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message) throws IOException {
        System.out.println(message.getPayload());
        session.sendMessage(new TextMessage("Hello"));
    }

}

```
