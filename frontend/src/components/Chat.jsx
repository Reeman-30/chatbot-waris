export default function Chat({ data }) {
	return (
		<>
			{data.map((val, index) => (
				<div
					className={`chat ${
						val.role === "amana" ? "chat-start" : "chat-end"
					} my-3`}
					key={index}
				>
					<div className="chat-bubble">
						{val.role === "user" ? (
							val.pertanyaan
						) : (
							<>
								<div>{val.responses?.response}</div>
								{val.responses.penjelasan_fiqh_with_hitungan ? (
									<div className="mt-2">
										{val.responses.penjelasan_fiqh_with_hitungan
											.split("\n")
											.map((line, i) => (
												<span key={i}>
													{line} <br />{" "}
												</span>
											))}
									</div>
								) : (
									""
								)}
							</>
						)}
					</div>
				</div>
			))}
		</>
	);
}
