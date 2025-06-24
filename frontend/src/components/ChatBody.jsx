import { React, useEffect, useRef, useState } from "react";
import axios from "axios";
import Chat from "./Chat";

function ChatBody() {
	const [pertanyaan, setPertanyaan] = useState({ teks: "" });
	const [messages, setMessages] = useState([
		{
			role: "amana",
			pertanyaan: null,
			confidence: 1.0,
			intent: "intro",
			responses: {
				response:
					"Assalamualaikum! Perkenalkan saya Amana, chatbot yang akan membantu Anda dalam melakukan perhitungan dan pembagian harta waris!",
				penjelasan_fiqh_with_hitungan: null,
			},
			entitas: null,
		},
	]);

	const HandlerSubmit = (e) => {
		e.preventDefault();
		HITUNG_WARIS();
	};

	const HITUNG_WARIS = async () => {
		try {
			const response = await axios({
				method: "post",
				maxBodyLength: Infinity,
				url: "http://localhost:5000/hitung_waris",
				headers: {
					"Content-Type": "application/json",
				},
				data: {
					teks: pertanyaan.teks,
				},
			});

			const userMessage = {
				role: "user",
				confidence: 1.0,
				intent: "pertanyaan",
				pertanyaan: pertanyaan.teks,
			};

			const amanaMessage = response.data;

			console.log(amanaMessage);
			const newMessages = [...messages, userMessage];
			setMessages(newMessages);
			setPertanyaan({ teks: "" });

			const messagesResponse = [...newMessages, amanaMessage];

			setTimeout(() => {
				setMessages(messagesResponse);
			}, 2000);

			console.log(messagesResponse);
		} catch (error) {
			alert(error.message);
			console.error(error.message);
		}
	};

	const endMessageRef = useRef(null);
	const scrollToBottom = () => {
		endMessageRef.current?.scrollIntoView({
			behaviour: "smooth",
		});
	};

	useEffect(() => {
		scrollToBottom();
	}, [messages]);

	return (
		<div className="container mx-auto p-5 fixed inset-0">
			<h1 className="text-center text-2xl font-bold">Chatbot Amana</h1>
			<div className="w-full h-full flex flex-col p-5">
				<div className="p-5 pb-8 flex-grow overflow-auto">
					<Chat data={messages} />
					<div ref={endMessageRef} />
				</div>
				<form
					method="POST"
					className="form-control m-5 text-center"
					onSubmit={(e) => HandlerSubmit(e)}
				>
					<div className="input-group w-full">
						<input
							type="text"
							placeholder="Silahkan isi pertanyaan"
							className="input input-bordered flex-grow w-5/6"
							value={pertanyaan.teks}
							onChange={(e) => setPertanyaan({ teks: e.target.value })}
							required
						/>
						<button className="btn btn-square" type="submit">
							<i className="bi bi-send"></i>
						</button>
					</div>
				</form>
				<div className="copyright text-center">
					<p className="font-light text-sm">
						Chatbot ini masih dalam tahap pengembangan
					</p>
					<span>&copy; 2025</span>
				</div>
			</div>
		</div>
	);
}

export default ChatBody;
