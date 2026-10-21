import SwiftUI
import PhotosUI
import Security

struct Card: Identifiable, Codable {
    let slug: String
    let name: String
    let keywords: [String]
    let meaning: String
    var id: String { slug }
}
struct Drawn: Identifiable {
    let card: Card
    let position: String
    let reversed: Bool
    var id: String { position + card.slug }
}
enum Tarot {
    static let cards: [Card] = [
        ("the-fool","The Fool","beginnings,curiosity,leap of faith","新しい流れに飛び込む勇気が、停滞を動かします。"),
        ("the-magician","The Magician","willpower,focus,manifestation","自分の意思と技術を一点に集めるほど結果が現れます。"),
        ("the-high-priestess","The High Priestess","intuition,inner voice,mystery","外側の情報より、自分の違和感や直感を優先する局面です。"),
        ("the-empress","The Empress","growth,nurture,abundance","育てる姿勢が人間関係や仕事の成果を豊かにします。"),
        ("the-emperor","The Emperor","structure,authority,stability","感情よりもルールと段取りを整えることで前進できます。"),
        ("the-hierophant","The Hierophant","tradition,teaching,guidance","基本に立ち返り、信頼できる型や助言を取り入れることで道筋が見えます。"),
        ("the-lovers","The Lovers","choice,alignment,relationship","大切なのは好かれることより、自分の価値観に合う選択です。"),
        ("the-chariot","The Chariot","momentum,discipline,victory","迷いを減らして一点突破すると、状況を動かせます。"),
        ("strength","Strength","patience,courage,gentle control","強引さより、粘り強く向き合う姿勢が勝ち筋になります。"),
        ("the-hermit","The Hermit","reflection,solitude,wisdom","結論を急がず、ひとりで考える時間が精度を上げます。"),
        ("wheel-of-fortune","Wheel of Fortune","change,timing,turning point","運の波は変わり始めています。流れを読むことが重要です。"),
        ("justice","Justice","fairness,truth,accountability","感情だけでなく事実と責任の線引きを明確にするほど道が開けます。"),
        ("the-hanged-man","The Hanged Man","pause,surrender,new perspective","急いで動くより、見方を変えるための停止が状況を好転させます。"),
        ("death","Death","ending,transition,renewal","終わらせるべき流れを手放すことで、次の始まりに入れます。"),
        ("temperance","Temperance","balance,moderation,integration","極端に振れず、異なる要素を丁寧に混ぜ合わせる姿勢が鍵です。"),
        ("the-devil","The Devil","attachment,temptation,shadow","自分を縛っている習慣や執着を自覚すると、主導権を取り戻せます。"),
        ("the-tower","The Tower","shock,collapse,awakening","無理に保っていた前提が崩れることで、本質に立ち返る機会が来ます。"),
        ("the-star","The Star","hope,healing,guidance","先を急がず、回復と希望を信じるほど流れは静かに整います。"),
        ("the-moon","The Moon","uncertainty,intuition,subconscious","見えない不安に飲まれず、曖昧さの中で直感を磨くことが大切です。"),
        ("the-sun","The Sun","clarity,joy,success","素直さと明るさを前に出すほど、状況は分かりやすく前進します。"),
        ("judgement","Judgement","calling,reflection,rebirth","過去の流れを見直し、いま本当に応えるべき呼びかけに向き合う時です。"),
        ("the-world","The World","completion,integration,fulfillment","これまでの積み重ねがまとまり、ひとつの完成へ近づいています。")
    ].map { Card(slug:$0.0,name:$0.1,keywords:$0.2.split(separator:",").map(String.init),meaning:$0.3) }
    static func draw(_ positions:[String]) -> [Drawn] {
        zip(cards.shuffled().prefix(positions.count),positions).map { Drawn(card:$0.0,position:$0.1,reversed:Bool.random()) }
    }
    static func reading(_ question:String,_ drawn:[Drawn])->String {
        "「\(question)」について\n\n" + drawn.map { "\($0.position)：\($0.card.name) \($0.reversed ? "逆位置":"正位置")\n\($0.card.meaning)\nキーワード：\($0.card.keywords.joined(separator:" / "))" }.joined(separator:"\n\n")
    }
}
enum Secrets {
    static let service="com.moonarcana.offline.openrouter"
    static var apiKey:String {
        get {
            let query:[String:Any]=[kSecClass as String:kSecClassGenericPassword,kSecAttrService as String:service,kSecReturnData as String:true,kSecMatchLimit as String:kSecMatchLimitOne]
            var result:CFTypeRef?
            guard SecItemCopyMatching(query as CFDictionary,&result)==errSecSuccess,let data=result as? Data else{return ""}
            return String(data:data,encoding:.utf8) ?? ""
        }
        set {
            let query:[String:Any]=[kSecClass as String:kSecClassGenericPassword,kSecAttrService as String:service]
            SecItemDelete(query as CFDictionary)
            if !newValue.isEmpty {
                var item=query
                item[kSecValueData as String]=Data(newValue.utf8)
                item[kSecAttrAccessible as String]=kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
                SecItemAdd(item as CFDictionary,nil)
            }
        }
    }
}
enum OpenRouter {
    static func request(model:String,key:String,question:String,drawn:[Drawn]?=nil,left:Data?=nil,right:Data?=nil) async throws -> String {
        guard !key.isEmpty else {throw NSError(domain:"OpenRouter APIキーを設定してください",code:1)}
        let prompt:String
        var content:[[String:Any]]=[]
        if let drawn {
            let cards=drawn.map { "\($0.position): \($0.card.name) \($0.reversed ? "reversed":"upright"); keywords=\($0.card.keywords.joined(separator:", ")); base=\($0.card.meaning)" }.joined(separator:"\n")
            prompt="あなたはMoon Arcanaのタロット解説AIです。占いを断定的な予言として扱わず、相談者が考えるための材料として、日本語で具体的かつ丁寧に解説してください。\n質問: \(question)\nカード:\n\(cards)\n構成: 1.全体像 2.各カードのつながり 3.注意点 4.今日からできる行動。800〜1200字程度。"
        } else {
            prompt="あなたはMoon Arcanaの手相占いAIです。添付された手のひら画像を観察し、見える範囲だけを根拠に日本語で丁寧に読み解いてください。断定的な未来予測、医療・健康診断、寿命の断定はしないでください。\n相談内容: \(question)\n構成: 1.左手 2.右手 3.総合リーディング 4.次の一歩。生命線・知能線・感情線・運命線など、画像から確認できる線を中心に説明してください。"
        }
        content.append(["type":"text","text":prompt])
        for data in [left,right].compactMap({$0}) {
            content.append(["type":"image_url","image_url":["url":"data:image/jpeg;base64,"+data.base64EncodedString()]])
        }
        let body:[String:Any]=["model":model,"messages":[["role":"user","content":drawn == nil ? content as Any : prompt as Any]],"temperature":0.7,"max_tokens":1800]
        var req=URLRequest(url:URL(string:"https://openrouter.ai/api/v1/chat/completions")!)
        req.httpMethod="POST"
        req.timeoutInterval=110
        req.setValue("Bearer "+key,forHTTPHeaderField:"Authorization")
        req.setValue("application/json",forHTTPHeaderField:"Content-Type")
        req.setValue("Moon Arcana iOS",forHTTPHeaderField:"X-Title")
        req.httpBody=try JSONSerialization.data(withJSONObject:body)
        let (data,response)=try await URLSession.shared.data(for:req)
        guard let http=response as? HTTPURLResponse,http.statusCode == 200 else {
            throw NSError(domain:"OpenRouter: "+String((String(data:data,encoding:.utf8) ?? "").prefix(300)),code:2)
        }
        let obj=try JSONSerialization.jsonObject(with:data) as? [String:Any]
        let choices=obj?["choices"] as? [[String:Any]]
        let message=choices?.first?["message"] as? [String:Any]
        return message?["content"] as? String ?? ""
    }
}
struct SavedReading: Codable, Identifiable {
    var id=UUID()
    let date:Date
    let question:String
    let cards:String
    let local:String
    let ai:String?
}
@MainActor final class AppState:ObservableObject {
    @Published var screen="home"
    @Published var question=""
    @Published var drawn:[Drawn]=[]
    @Published var local=""
    @Published var aiText=""
    @Published var error=""
    @Published var busy=false
    @Published var left:Data?
    @Published var right:Data?
    @Published var history:[SavedReading]=[]
    @Published var model=UserDefaults.standard.string(forKey:"model") ?? "openai/gpt-4.1-mini" {
        didSet {UserDefaults.standard.set(model,forKey:"model")}
    }
    func begin(_ positions:[String]) {drawn=[];aiText="";screen="draw";pending=positions}
    var pending:[String]=[]
    func draw(){drawn=Tarot.draw(pending);local=Tarot.reading(question,drawn);screen="result"}
    func save(ai:String?=nil){
        let cards=drawn.map{"\($0.card.name)(\($0.reversed ? "逆":"正"))"}.joined(separator:" / ")
        history.insert(SavedReading(date:Date(),question:question,cards:cards,local:local,ai:ai),at:0)
        if history.count>30 {history=Array(history.prefix(30))}
        if let data=try? JSONEncoder().encode(history){UserDefaults.standard.set(data,forKey:"readings")}
    }
    init(){if let data=UserDefaults.standard.data(forKey:"readings"),let h=try? JSONDecoder().decode([SavedReading].self,from:data){history=h}}
    func interpret(palm:Bool=false){
        busy=true;error=""
        let model=model,key=Secrets.apiKey,question=question,drawn=drawn,left=left,right=right
        Task {
            do {aiText=try await OpenRouter.request(model:model,key:key,question:question,drawn:palm ? nil : drawn,left:palm ? left : nil,right:palm ? right : nil)}
            catch {self.error=error.localizedDescription}
            busy=false
        }
    }
}
@main struct MoonArcanaApp:App {
    @StateObject private var state=AppState()
    var body:some Scene {WindowGroup{MainView().environmentObject(state)}}
}
struct MainView:View {
    @EnvironmentObject var state:AppState
    @State private var keyInput=""
    @State private var customModel=""
    @State private var leftPhoto:PhotosPickerItem?
    @State private var rightPhoto:PhotosPickerItem?
    let bg=Color(red:13/255,green:9/255,blue:29/255)
    let gold=Color(red:241/255,green:194/255,blue:92/255)
    let panel=Color(red:28/255,green:20/255,blue:51/255)
    let models:[(String,String)]=[
        ("GPT-4.1 mini","openai/gpt-4.1-mini"),("GPT-4.1","openai/gpt-4.1"),("GPT-4.1 nano","openai/gpt-4.1-nano"),("Gemini 3 Flash Preview","google/gemini-3-flash-preview"),("Gemini 2.5 Flash","google/gemini-2.5-flash"),("Gemini 2.5 Pro","google/gemini-2.5-pro"),("Claude Sonnet 4","anthropic/claude-sonnet-4"),("DeepSeek Chat V3","deepseek/deepseek-chat-v3-0324")]
    var body:some View {
        ScrollView {
            VStack(spacing:16) {
                Text("✦  \(title)  ✦").font(.system(size:28,weight:.bold)).foregroundStyle(gold).multilineTextAlignment(.center)
                switch state.screen {
                case "home":home
                case "draw":draw
                case "result":result
                case "palm":palm
                case "history":history
                case "settings":settings
                default:home
                }
                if state.screen != "home" { secondary("← ホーム"){state.screen="home"} }
            }.padding(22).frame(maxWidth:.infinity)
        }.background(bg).foregroundStyle(.white)
            .alert("エラー",isPresented:Binding(get:{!state.error.isEmpty},set:{if !$0 {state.error=""}})){Button("OK"){state.error=""}}message:{Text(state.error)}
            .onChange(of:leftPhoto){item in Task{state.left=await jpeg(item)}}
            .onChange(of:rightPhoto){item in Task{state.right=await jpeg(item)}}
    }
    var title:String {
        switch state.screen {case "draw":return "カードを引く";case "result":return "占い結果";case "palm":return "手相占い";case "history":return "占い履歴";case "settings":return "AIモデル設定";default:return "Moon Arcana"}
    }
    func primary(_ label:String,_ action:@escaping ()->Void)->some View {
        Button(action:action){Text(label).frame(maxWidth:.infinity).padding(16).foregroundStyle(bg).background(gold,in:RoundedRectangle(cornerRadius:18))}
    }
    func secondary(_ label:String,_ action:@escaping ()->Void)->some View {
        Button(action:action){Text(label).frame(maxWidth:.infinity).padding(16).background(Color(red:49/255,green:37/255,blue:75/255),in:RoundedRectangle(cornerRadius:18))}
    }
    func heading(_ text:String)->some View {Text(text).font(.headline).foregroundStyle(gold).padding(.top,10)}
    var home:some View {
        VStack(spacing:12){
            Text("☾").font(.system(size:44)).foregroundStyle(gold)
            Text("今、いちばん知りたいことは何ですか？")
            heading("YOUR QUESTION")
            TextEditor(text:$state.question).scrollContentBackground(.hidden).frame(height:110).padding(8).background(panel,in:RoundedRectangle(cornerRadius:18))
            heading("TAROT READING")
            primary("✦ 1枚引き"){start(["焦点"],fallback:"今日の運勢")}
            primary("✦ 3枚引き — 過去・現在・未来"){start(["過去","現在","未来"],fallback:"今の流れ")}
            primary("✦ 5枚引き — 総合"){start(["現状","障害","隠れた要因","アドバイス","今後の流れ"],fallback:"総合運")}
            heading("SPECIAL READING")
            secondary("仕事運 5枚引き"){start(["現状","強み・追い風","課題・障害","取るべき行動","今後の仕事運"],fallback:"仕事運")}
            secondary("復縁 5枚引き"){start(["相手の気持ち","復縁の可能性","障害","あなたの一手","今後の流れ"],fallback:"復縁について")}
            secondary("✋ 手相占い — 写真からAI鑑定"){if state.question.trimmingCharacters(in:.whitespacesAndNewlines).isEmpty{state.question="手相から今の流れを知りたい"};state.screen="palm"}
            heading("MY ARCANA")
            secondary("占い履歴"){state.screen="history"}
            secondary("AIモデル・OpenRouter設定"){state.screen="settings"}
            Text("カードと履歴はオフライン。AI詳細解説と手相鑑定のみOpenRouterに接続します。").font(.caption).foregroundStyle(.gray)
        }
    }
    func start(_ positions:[String],fallback:String){if state.question.trimmingCharacters(in:.whitespacesAndNewlines).isEmpty{state.question=fallback};state.begin(positions)}
    var draw:some View {
        VStack(spacing:16){Text("質問：\(state.question)");primary("この質問でカードを引く"){state.draw()};secondary("← 質問を変更"){state.screen="home"}}
    }
    var result:some View {
        VStack(spacing:14){
            Text("「\(state.question)」").foregroundStyle(gold)
            ForEach(state.drawn){d in
                VStack(spacing:10){
                    Text(d.position).foregroundStyle(gold)
                    Text(d.card.name).font(.title2.bold())
                    Text(d.reversed ? "逆位置":"正位置")
                    Image(d.card.slug.replacingOccurrences(of:"-",with:"_")).resizable().scaledToFit().frame(maxHeight:350).rotationEffect(.degrees(d.reversed ? 180:0))
                    Text(d.card.keywords.joined(separator:" · ")).foregroundStyle(gold)
                    Text(d.card.meaning)
                }.frame(maxWidth:.infinity).padding(16).background(panel,in:RoundedRectangle(cornerRadius:22))
            }
            heading("READING")
            Text(state.local)
            primary("この結果を端末に保存"){state.save()}
            ShareLink(item:shareText){Text("𝕏 占い結果をXにシェア").frame(maxWidth:.infinity).padding(16).background(panel,in:RoundedRectangle(cornerRadius:18))}
            primary("AIで詳細解説 · \(state.model.components(separatedBy:"/").last ?? "")"){state.interpret()}
            if state.busy {ProgressView().tint(gold)}
            if !state.aiText.isEmpty {heading("AI READING");Text(state.aiText);primary("AI解説込みで保存"){state.save(ai:state.aiText)}}
        }
    }
    var shareText:String {"🔮 Moon Arcanaの占い結果\n質問：\(state.question)\n"+state.drawn.map{"・\($0.position)：\($0.card.name)（\($0.reversed ? "逆位置":"正位置")）"}.joined(separator:"\n")+"\n\n#MoonArcana #タロット占い"}
    var palm:some View {
        VStack(spacing:14){
            Text("質問：\(state.question)")
            heading("左手")
            PhotosPicker(selection:$leftPhoto,matching:.images){Text(state.left == nil ? "写真を選ぶ":"写真を変更")}
            if let d=state.left,let img=UIImage(data:d){Image(uiImage:img).resizable().scaledToFit().frame(maxHeight:250)}
            heading("右手")
            PhotosPicker(selection:$rightPhoto,matching:.images){Text(state.right == nil ? "写真を選ぶ":"写真を変更")}
            if let d=state.right,let img=UIImage(data:d){Image(uiImage:img).resizable().scaledToFit().frame(maxHeight:250)}
            Text("片手だけでも鑑定できます。両手を登録すると左右を比較して読み解きます。").font(.caption)
            primary("AIで手相を鑑定"){if state.left == nil && state.right == nil{state.error="手のひらの写真を1枚以上選択してください"}else{state.interpret(palm:true)}}
            if state.busy {ProgressView().tint(gold)}
            if !state.aiText.isEmpty {heading("PALM READING");Text(state.aiText)}
        }
    }
    func jpeg(_ item:PhotosPickerItem?) async -> Data? {
        guard let data=try? await item?.loadTransferable(type:Data.self),let img=UIImage(data:data) else{return nil}
        let ratio=min(1,1600/max(img.size.width,img.size.height))
        let size=CGSize(width:img.size.width*ratio,height:img.size.height*ratio)
        let renderer=UIGraphicsImageRenderer(size:size)
        return renderer.jpegData(withCompressionQuality:0.86){_ in img.draw(in:CGRect(origin:.zero,size:size))}
    }
    var history:some View {
        VStack(spacing:14){
            if state.history.isEmpty{Text("まだ履歴はありません。")}
            ForEach(state.history){h in
                VStack(alignment:.leading,spacing:8){Text(h.date.formatted(date:.numeric,time:.shortened)).foregroundStyle(gold);Text(h.question);Text(h.cards);Text(h.ai ?? h.local)}
                    .frame(maxWidth:.infinity,alignment:.leading).padding().background(panel,in:RoundedRectangle(cornerRadius:18))
            }
        }
    }
    var settings:some View {
        VStack(spacing:14){
            Text("現在のモデル\n\(state.model)").foregroundStyle(gold)
            SecureField("OpenRouter API key (sk-or-v1-...)",text:$keyInput).textInputAutocapitalization(.never).padding().background(panel,in:RoundedRectangle(cornerRadius:16))
            primary("APIキーを保存"){if !keyInput.isEmpty{Secrets.apiKey=keyInput;keyInput=""}}
            heading("MODEL")
            ForEach(models.indices,id:\.self){i in secondary(models[i].0){state.model=models[i].1}}
            TextField("その他のモデルID",text:$customModel).textInputAutocapitalization(.never).padding().background(panel,in:RoundedRectangle(cornerRadius:16))
            secondary("カスタムモデルを保存"){if !customModel.isEmpty{state.model=customModel}}
        }
    }
}
