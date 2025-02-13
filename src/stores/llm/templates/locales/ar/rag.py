from string import Template

######## RAG PROMPTS ########

##### SYSTEM #####

system_prompt = Template("\n".join([
    "أنت مساعد لتوليد رد للمستخدم.",
    "سيتم تزويدك بمجموعة من الوثائق المرتبطة باستعلام المستخدم.",
    "عليك توليد رد بناءً على الوثائق المقدمة.",
    "تجاهل الوثائق غير المرتبطة باستعلام المستخدم.",
    "يمكنك الاعتذار للمستخدم إذا لم تتمكن من توليد رد.",
    "يجب أن تولد الرد بنفس لغة استعلام المستخدم.",
    "كن مهذبًا ومحترمًا تجاه المستخدم.",
    "كن دقيقًا وموجزًا في ردك. تجنب المعلومات غير الضرورية.",
    ]
))

##### DOCUMENT #####

document_prompt = Template(
    "\n".join([
        "## رقم الوثيقة: $doc_num",
        "### المحتوى: $chunk_text",
    ])
)

##### FOOTER #####

footer_prompt = Template(
    "\n".join([
        "بناءً فقط على الوثائق المذكورة أعلاه، يرجى توليد إجابة للمستخدم.",
        "# السؤال",
        "",
        "## الإجابة:"

    ])
)
