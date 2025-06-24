import React from "react";
import { Route, Routes } from "react-router-dom";
import ChatBody from "../components/ChatBody";

export default function AppRoute() {
	return (
		<Routes>
			<Route index element={<WelcomePage />} />
			<Route path="chatbot-waris" element={<ChatBody />} />
		</Routes>
	);
}

const WelcomePage = () => {
	return (
		<div className="min-h-screen flex items-center justify-center bg-gray-800 text-white">
			<div className="text-center">
				<h1 className="text-5xl font-bold">Selamat Datang!</h1>
				<p className="mt-2 text-lg">Saya Amana! Chatbot Warisan Islam</p>
				<a href="/chatbot-waris">
					<button className="btn btn-primary my-5">Mulai Chat!</button>
				</a>
			</div>
		</div>
	);
};
